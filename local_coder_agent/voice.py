from __future__ import annotations

import os
import shlex
import subprocess
from typing import Optional


class SpeechIO:
    """Thin voice wrapper for local dictation and TTS.

    This keeps the local-first design explicit: any real speech input/output is
    performed on this machine, not via cloud transcription or a remote TTS API.
    """

    def __init__(self, tts_command: Optional[str] = None) -> None:
        self.tts_command = tts_command or os.getenv("LOCAL_TTS_COMMAND", "espeak-ng -s 160 -v en-us")

    def listen(self, timeout: int = 10) -> str:
        try:
            import speech_recognition as sr
        except ImportError as exc:  # pragma: no cover - runtime dependency may be missing
            raise RuntimeError(
                "voice dictation requires speech_recognition. Install the agent requirements first."
            ) from exc

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=timeout)

        try:
            return recognizer.recognize_google(audio)
        except Exception:
            return recognizer.recognize_sphinx(audio)

    def speak(self, text: str) -> None:
        if not text.strip():
            return

        command = f"{self.tts_command} {shlex.quote(text)}"
        subprocess.run(command, shell=True, check=False)
