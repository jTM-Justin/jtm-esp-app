#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClient.h>

#include "config.h"

WiFiClient client;

enum class BootState {
  BOOTING,
  WIFI_CONNECTING,
  WIFI_READY,
  TUNNEL_READY,
  DEPLOY_READY
};

namespace {
struct LedState {
  int targetBrightness = 0;
  int currentBrightness = 0;
  unsigned long lastUpdate = 0;
};

LedState ledState;
BootState currentBootState = BootState::BOOTING;

void setLedBrightness(int brightness) {
  brightness = constrain(brightness, ESP32S3_LED_MIN_BRIGHTNESS, ESP32S3_LED_MAX_BRIGHTNESS);
  analogWrite(ESP32S3_LED_PIN, brightness);
}

void updateLedState(int targetBrightness) {
  if (ledState.targetBrightness == targetBrightness && ledState.currentBrightness == targetBrightness) {
    return;
  }

  ledState.targetBrightness = targetBrightness;
  ledState.lastUpdate = millis();
}

void tickLed() {
  const unsigned long now = millis();
  const int target = ledState.targetBrightness;

  if (ledState.currentBrightness != target) {
    const float step = (float)(target - ledState.currentBrightness) / (float)(ESP32S3_LED_FADE_MS / 20);
    ledState.currentBrightness += (int)step;
    if ((step > 0 && ledState.currentBrightness > target) || (step < 0 && ledState.currentBrightness < target)) {
      ledState.currentBrightness = target;
    }
    setLedBrightness(ledState.currentBrightness);
  }

  if (now - ledState.lastUpdate > ESP32S3_LED_FADE_MS) {
    ledState.lastUpdate = now;
  }
}

void setBootState(BootState nextState) {
  if (currentBootState == nextState) {
    return;
  }

  currentBootState = nextState;

  switch (nextState) {
    case BootState::BOOTING:
      Serial.println("Booting...");
      updateLedState(ESP32S3_LED_MIN_BRIGHTNESS);
      break;
    case BootState::WIFI_CONNECTING:
      Serial.println("Wi-Fi connecting...");
      updateLedState(ESP32S3_LED_MIN_BRIGHTNESS);
      break;
    case BootState::WIFI_READY:
      Serial.println("Wi-Fi ready");
      updateLedState(ESP32S3_LED_WIFI_CONNECTED_BRIGHTNESS);
      break;
    case BootState::TUNNEL_READY:
      Serial.println("Tunnel connected");
      updateLedState(ESP32S3_LED_TUNNEL_CONNECTED_BRIGHTNESS);
      break;
    case BootState::DEPLOY_READY:
      Serial.println("Deployment ready");
      updateLedState(ESP32S3_LED_DEPLOY_READY_BRIGHTNESS);
      break;
  }
}
}

void connectToWiFi() {
  IPAddress localIp;
  IPAddress gateway;
  IPAddress subnet;

  setBootState(BootState::WIFI_CONNECTING);
  localIp.fromString(ESP32S3_KEYBOARD_LOCAL_IP);
  gateway.fromString(ESP32S3_KEYBOARD_GATEWAY);
  subnet.fromString(ESP32S3_KEYBOARD_SUBNET);

  WiFi.mode(WIFI_STA);
  WiFi.config(localIp, gateway, subnet);
  WiFi.begin(ESP32S3_KEYBOARD_WIFI_SSID, ESP32S3_KEYBOARD_WIFI_PASSWORD);

  Serial.println("Connecting to Wi-Fi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
    Serial.print(".");
    updateLedState(ESP32S3_LED_MIN_BRIGHTNESS);
    tickLed();
  }

  Serial.println();
  Serial.printf("Wi-Fi connected: %s\n", WiFi.localIP().toString().c_str());
  setBootState(BootState::WIFI_READY);
}

bool sendKeyboardEvent(const char *key) {
  if (!client.connected()) {
    if (!client.connect(ESP32S3_KEYBOARD_TARGET_IP, ESP32S3_KEYBOARD_TARGET_PORT)) {
      Serial.printf("Failed to connect to %s:%d\n",
                    ESP32S3_KEYBOARD_TARGET_IP,
                    ESP32S3_KEYBOARD_TARGET_PORT);
      setBootState(BootState::WIFI_READY);
      updateLedState(ESP32S3_LED_MIN_BRIGHTNESS);
      return false;
    }
    setBootState(BootState::TUNNEL_READY);
  }

  client.printf("POST %s HTTP/1.1\r\n", ESP32S3_KEYBOARD_PATH);
  client.printf("Host: %s:%d\r\n", ESP32S3_KEYBOARD_TARGET_IP, ESP32S3_KEYBOARD_TARGET_PORT);
  client.println("Content-Type: application/json");
  client.println("Connection: close");
  client.print("Content-Length: ");
  client.println(strlen(key) + 32);
  client.println();
  client.printf("{\"type\":\"keyboard\",\"key\":\"%s\"}\r\n", key);
  setBootState(BootState::DEPLOY_READY);
  updateLedState(ESP32S3_LED_INPUT_ACTIVE_BRIGHTNESS);
  return true;
}

void setup() {
  Serial.begin(115200);
  pinMode(ESP32S3_LED_PIN, OUTPUT);
  analogWrite(ESP32S3_LED_PIN, ESP32S3_LED_MIN_BRIGHTNESS);
  ledState.currentBrightness = ESP32S3_LED_MIN_BRIGHTNESS;
  ledState.targetBrightness = ESP32S3_LED_MIN_BRIGHTNESS;
  setBootState(BootState::BOOTING);
  delay(ESP32S3_KEYBOARD_BOOT_DELAY_MS);

  Serial.println("ESP32 keyboard booting...");
  Serial.printf("Tunnel target = %s:%d%s\n",
                ESP32S3_KEYBOARD_TARGET_IP,
                ESP32S3_KEYBOARD_TARGET_PORT,
                ESP32S3_KEYBOARD_PATH);

  connectToWiFi();
  sendKeyboardEvent(ESP32S3_KEYBOARD_READY_SIGNAL);
}

void loop() {
  static unsigned long lastSend = 0;
  const char *demoKey = "A";

  tickLed();

  if (millis() - lastSend > 3000) {
    sendKeyboardEvent(demoKey);
    lastSend = millis();
  }

  if (currentBootState == BootState::DEPLOY_READY && millis() - lastSend > 100) {
    updateLedState(ESP32S3_LED_DEPLOY_READY_BRIGHTNESS);
  }

  delay(ESP32S3_KEYBOARD_POLL_MS);
}
