from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TunnelConfig:
    tunnel_name: str = "jtm-esp"
    hostname: str = "jtm-esp.example.com"
    secure: bool = True

    @property
    def url(self) -> str:
        protocol = "https" if self.secure else "http"
        return f"{protocol}://{self.hostname}"


def build_status(tunnel_name: str = "jtm-esp", hostname: str | None = None, secure: bool = True) -> dict[str, object]:
    config = TunnelConfig(tunnel_name=tunnel_name, hostname=hostname or "jtm-esp.example.com", secure=secure)
    return {
        "tunnel_name": config.tunnel_name,
        "hostname": config.hostname,
        "secure": config.secure,
        "url": config.url,
        "status": "ready" if config.secure else "warning",
    }
