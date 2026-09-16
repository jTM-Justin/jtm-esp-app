from __future__ import annotations

import json
import os
import subprocess
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


@dataclass(frozen=True)
class AgentConfig:
    planner_model: str = "hermes3"
    coder_model: str = "qwen2.5-coder"
    api_base: str = OLLAMA_BASE_URL
    working_directory: str = "."


class OllamaClient:
    def __init__(self, config: AgentConfig | None = None) -> None:
        self.config = config or AgentConfig()

    def _request(self, model: str, prompt: str) -> str:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        }
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{self.config.api_base}/api/chat",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
                message = data.get("message", {}).get("content", "")
                return message.strip()
        except Exception as exc:  # pragma: no cover - used in live environment
            return f"Local Ollama model unavailable: {exc}"

    def plan(self, task: str) -> str:
        prompt = (
            "You are the planner for a local-first coding agent. "
            "Break the task into a safe, minimal set of steps and return only the plan.\n\n"
            f"Task: {task}"
        )
        return self._request(self.config.planner_model, prompt)

    def code(self, task: str, context: str = "") -> str:
        prompt = (
            "You are a local coding agent. Produce a concise, executable patch or shell command plan "
            "for the task. Keep it practical and specific.\n\n"
            f"Task: {task}\n\nContext:\n{context}"
        )
        return self._request(self.config.coder_model, prompt)


class LocalCodingAgent:
    def __init__(self, config: AgentConfig | None = None) -> None:
        self.config = config or AgentConfig()
        self.ollama = OllamaClient(self.config)

    def run_shell(self, command: str) -> str:
        completed = subprocess.run(command, shell=True, cwd=self.config.working_directory, capture_output=True, text=True)
        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()
        return stdout or stderr or "command finished with no output"

    def read_file(self, path: str) -> str:
        return Path(path).read_text(encoding="utf-8")

    def write_file(self, path: str, content: str) -> str:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        return f"updated {path}"

    def execute_task(self, task: str) -> dict[str, str]:
        plan = self.ollama.plan(task)
        code = self.ollama.code(task, plan)
        return {"plan": plan, "code": code}

    def interactive_loop(self) -> None:
        while True:
            try:
                user_task = input("local-agent> ")
            except EOFError:
                break
            if not user_task.strip():
                continue
            result = self.execute_task(user_task)
            print("PLAN:\n" + result["plan"])
            print("CODE:\n" + result["code"])
            if user_task.lower().strip() in {"quit", "exit"}:
                break


def main() -> int:
    agent = LocalCodingAgent()
    agent.interactive_loop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
