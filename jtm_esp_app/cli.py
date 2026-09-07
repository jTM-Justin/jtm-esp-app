from __future__ import annotations

import argparse
import json

from .bridge import build_status
from .keyboard import KeyboardBuffer, KeyboardEvent


def _demo_events() -> list[KeyboardEvent]:
    return [
        KeyboardEvent("H", True),
        KeyboardEvent("i", True),
        KeyboardEvent("!", True),
        KeyboardEvent("A", True),
        KeyboardEvent("I", True),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the simple ESP keyboard tunnel app.")
    parser.add_argument("--tunnel-name", default="jtm-esp")
    parser.add_argument("--hostname", default="jtm-esp.example.com")
    parser.add_argument("--insecure", action="store_true", help="disable secure HTTPS tunnel URL")
    parser.add_argument("--demo", action="store_true", help="print a sample keyboard session")
    args = parser.parse_args()

    status = build_status(args.tunnel_name, args.hostname, secure=not args.insecure)
    if args.demo:
        buffer = KeyboardBuffer()
        buffer.record_many(_demo_events())
        status["keys"] = buffer.active_keys()
        status["typed_text"] = buffer.text()

    print(json.dumps(status, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
