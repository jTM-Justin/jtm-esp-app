from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class KeyboardEvent:
    key: str
    pressed: bool = True
    modifiers: tuple[str, ...] = ()

    def normalized_key(self) -> str:
        if not self.key:
            return ""
        key = self.key.strip()
        return key.lower() if key.isalpha() else key


@dataclass
class KeyboardBuffer:
    max_events: int = 32
    entries: list[KeyboardEvent] = field(default_factory=list)

    def record(self, event: KeyboardEvent) -> list[KeyboardEvent]:
        self.entries.append(event)
        if len(self.entries) > self.max_events:
            self.entries = self.entries[-self.max_events :]
        return self.entries.copy()

    def record_many(self, events: Iterable[KeyboardEvent]) -> list[KeyboardEvent]:
        for event in events:
            self.record(event)
        return self.entries.copy()

    def active_keys(self) -> list[str]:
        return [event.normalized_key() for event in self.entries if event.pressed and event.normalized_key()]

    def text(self) -> str:
        return "".join(self.active_keys())

    def clear(self) -> None:
        self.entries.clear()
