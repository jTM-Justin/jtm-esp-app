# ESP32-S3 USB HID Keyboard/Mouse Bridge

This project creates a USB HID bridge for an ESP32-S3 board with two USB-C ports. The board presents itself as a USB keyboard and mouse while forwarding input and output to a local service exposed through a Cloudflare tunnel.

## Network settings

- Local service IP: `192.168.1.100`
- Cloudflare tunnel port: `8080`
- Target bridge route: `http://192.168.1.100:8080/bridge`

## Hardware idea

- USB-C port 1: host connection for the downstream keyboard/mouse device
- USB-C port 2: USB client connection for the ESP32-S3 acting as a HID device
- ESP32-S3 runs the bridge firmware and submits keyboard/mouse reports over Wi-Fi to the local service
- The local service can then relay traffic to the Cloudflare tunnel on port 8080

## Firmware layout

- `src/config.h`: bridge settings
- `src/main.cpp`: Arduino/ESP32-S3 sketch

## Quick start

1. Install PlatformIO.
2. Open this folder as a PlatformIO project.
3. Update Wi-Fi credentials and tunnel endpoint values in `src/config.h`.
4. Build and upload to the ESP32-S3.

```bash
pio run -t upload
```

## Example sketch behavior

The firmware does the following:

- connects to Wi-Fi
- opens a TCP connection to `192.168.1.100:8080`
- advertises the ESP32-S3 as a USB HID keyboard and mouse
- sends HID reports to the bridge endpoint for remote processing
- sends acknowledgements back to the host device when data is received
