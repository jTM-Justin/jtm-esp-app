"""Local-first coding agent scaffold using Ollama models and voice I/O."""

from .agent import LocalCodingAgent, OllamaClient
from .voice import SpeechIO

__all__ = ["LocalCodingAgent", "OllamaClient", "SpeechIO"]
