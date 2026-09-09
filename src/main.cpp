#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClient.h>

#include "config.h"

WiFiClient client;

void connectToWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ESP32S3_KEYBOARD_WIFI_SSID, ESP32S3_KEYBOARD_WIFI_PASSWORD);

  Serial.println("Connecting to Wi-Fi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
    Serial.print(".");
  }

  Serial.println();
  Serial.printf("Wi-Fi connected: %s\n", WiFi.localIP().toString().c_str());
}

bool sendKeyboardEvent(const char *key) {
  if (!client.connected()) {
    if (!client.connect(ESP32S3_KEYBOARD_TARGET_IP, ESP32S3_KEYBOARD_TARGET_PORT)) {
      Serial.printf("Failed to connect to %s:%d\n",
                    ESP32S3_KEYBOARD_TARGET_IP,
                    ESP32S3_KEYBOARD_TARGET_PORT);
      return false;
    }
  }

  client.printf("POST %s HTTP/1.1\r\n", ESP32S3_KEYBOARD_PATH);
  client.printf("Host: %s:%d\r\n", ESP32S3_KEYBOARD_TARGET_IP, ESP32S3_KEYBOARD_TARGET_PORT);
  client.println("Content-Type: application/json");
  client.println("Connection: close");
  client.print("Content-Length: ");
  client.println(strlen(key) + 32);
  client.println();
  client.printf("{\"type\":\"keyboard\",\"key\":\"%s\"}\r\n", key);
  return true;
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("ESP32 keyboard booting...");
  Serial.printf("Tunnel target = %s:%d%s\n",
                ESP32S3_KEYBOARD_TARGET_IP,
                ESP32S3_KEYBOARD_TARGET_PORT,
                ESP32S3_KEYBOARD_PATH);

  connectToWiFi();
  sendKeyboardEvent("READY");
}

void loop() {
  static unsigned long lastSend = 0;
  const char *demoKey = "A";

  if (millis() - lastSend > 3000) {
    sendKeyboardEvent(demoKey);
    lastSend = millis();
  }

  delay(ESP32S3_KEYBOARD_POLL_MS);
}
