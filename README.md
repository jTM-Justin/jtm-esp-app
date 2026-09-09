# ESP32 Keyboard with Cloudflare Tunnel

This project is for a bare ESP32-S3 board with no screen, no microphone, and no speaker. It acts as a simple USB keyboard sender and sends keyboard events to a local service that is exposed through a Cloudflare tunnel.

## Target setup

- Board: ESP32-S3 bare dev board
- ESP32 local IP: `192.168.1.50`
- Local tunnel target: `192.168.1.100`
- Cloudflare tunnel port: `8080`
- Endpoint: `http://192.168.1.100:8080/keyboard`
- Hardware profile: no display, no mic, no speaker

## Boot and deploy flow

The firmware now follows a single ready path:

1. Boot starts in `BOOTING`
2. Wi‑Fi connects and moves to `WIFI_READY`
3. Tunnel connection moves to `TUNNEL_READY`
4. A successful deploy signal sends `READY` and settles at `DEPLOY_READY`

The LED stays dim and fades between states instead of flashing.

## Project files

- `platformio.ini` — PlatformIO config for the bare ESP32-S3
- `src/config.h` — current keyboard configuration
- `src/last_config.h` — saved last-known working configuration
- `src/main.cpp` — ESP32 keyboard firmware entry point

## Quick start

1. Install PlatformIO.
2. Open this folder as the project root.
3. Update Wi-Fi SSID/password in `src/config.h`.
4. Build and upload:

```bash
pio run -t upload
```

## Notes

This is deliberately a lightweight keyboard-only implementation. It does not use a screen or audio peripherals and is intended for a minimal bare ESP32-S3 setup.
