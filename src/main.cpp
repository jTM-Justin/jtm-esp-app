#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClient.h>

#include "config.h"

WiFiClient client;

void connectToWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ESP32S3_BRIDGE_WIFI_SSID, ESP32S3_BRIDGE_WIFI_PASSWORD);

  Serial.println("Connecting to Wi-Fi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
    Serial.print(".");
  }

  Serial.println();
  Serial.printf("Wi-Fi connected: %s\n", WiFi.localIP().toString().c_str());
}

bool connectToBridge() {
  if (!client.connect(ESP32S3_BRIDGE_TARGET_IP, ESP32S3_BRIDGE_TARGET_PORT)) {
    Serial.printf("Failed to connect to %s:%d\n", ESP32S3_BRIDGE_TARGET_IP, ESP32S3_BRIDGE_TARGET_PORT);
    return false;
  }

  Serial.printf("Connected to bridge at %s:%d\n", ESP32S3_BRIDGE_TARGET_IP, ESP32S3_BRIDGE_TARGET_PORT);
  client.println("POST " ESP32S3_BRIDGE_PATH " HTTP/1.1");
  client.printf("Host: %s:%d\r\n", ESP32S3_BRIDGE_TARGET_IP, ESP32S3_BRIDGE_TARGET_PORT);
  client.println("Content-Type: application/json");
  client.println("Connection: close");
  client.println();
  return true;
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("ESP32-S3 USB HID keyboard/mouse bridge starting...");
  Serial.printf("Target bridge = %s:%d%s\n",
                ESP32S3_BRIDGE_TARGET_IP,
                ESP32S3_BRIDGE_TARGET_PORT,
                ESP32S3_BRIDGE_PATH);

  connectToWiFi();
  connectToBridge();
}

void loop() {
  if (!client.connected()) {
    connectToBridge();
  }

  delay(ESP32S3_BRIDGE_POLL_MS);
}
