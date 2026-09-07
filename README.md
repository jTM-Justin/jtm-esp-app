# jtm-esp-app

A lightweight Python app for an AI-powered ESP32 keyboard workflow that uses secure Cloudflare tunnel routing and a local microcontroller programming setup.

## What this project includes

- A simple tunnel configuration model for secure HTTPS hostnames
- A keyboard event buffer that tracks typed keys from an ESP32 input flow
- A CLI entry point for a "try now" smoke test

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python app.py --demo
```

The demo prints a small status payload showing the tunnel URL and captured keyboard text.

## Example output

```json
{
  "hostname": "jtm-esp.example.com",
  "secure": true,
  "status": "ready",
  "tunnel_name": "jtm-esp",
  "typed_text": "hi!ai",
  "url": "https://jtm-esp.example.com"
}
```

## Tests

```bash
python -m unittest discover -s tests -v
```
