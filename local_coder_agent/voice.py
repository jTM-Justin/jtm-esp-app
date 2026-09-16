from __future__ import annotations

import os
import shlex
import subprocess
from typing import Optional


class SpeechIO:
    """Thin local-first voice wrapper for dictation and TTS.

    The default behavior intentionally favors a local speech stack over cloud-based
    transcription. The backend can be switched via the
    `VOICE_DICTATION_BACKEND` environment variable, with `voxtype` and `vosk`
    treated as equivalent aliases for a local dictation engine.
    """

    def __init__(self, tts_command: Optional[str] = None, dictation_backend: Optional[str] = None) -> None:
        self.tts_command = tts_command or os.getenv("LOCAL_TTS_COMMAND", "espeak-ng -s 160 -v en-us")
        backend = (dictation_backend or os.getenv("VOICE_DICTATION_BACKEND", "vosk") or "vosk").strip().lower()
        backend_aliases = {
            "voxtype": "vosk",
            "vox-type": "vosk",
            "voice-type": "vosk",
            "local": "vosk",
            "default": "vosk",
        }
        self.dictation_backend = backend_aliases.get(backend, backend)

    def listen(self, timeout: int = 10) -> str:
        if self.dictation_backend in {"cloud", "google"}:
            raise RuntimeError(
                "Cloud dictation is disabled for this local-first agent. "
                "Set VOICE_DICTATION_BACKEND=vosk (or voxtype) to use a local backend."
            )

        try:
            import speech_recognition as sr
        except ImportError as exc:  # pragma: no cover - runtime dependency may be missing
            raise RuntimeError(
                "voice dictation requires speech_recognition plus a local backend such as Vosk. "
                "Install the agent requirements and set VOICE_DICTATION_BACKEND=vosk."
            ) from exc

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=timeout)

        if self.dictation_backend in {"vosk", "local"}:
            if hasattr(recognizer, "recognize_vosk"):
                return recognizer.recognize_vosk(audio)
            raise RuntimeError(
                "Vosk support is not available. Install a local speech model and a compatible Vosk backend."
            )

        if hasattr(recognizer, "recognize_whisper"):
            return recognizer.recognize_whisper(audio)

        raise RuntimeError(
            "No supported local dictation backend is available. "
            "Install Vosk or a local Whisper backend and set VOICE_DICTATION_BACKEND accordingly."
        )

    def speak(self, text: str) -> None:
        if not text.strip():
            return

        command = f"{self.tts_command} {shlex.quote(text)}"
        subprocess.run(command, shell=True, check=False)
