import unittest

from local_coder_agent.agent import AgentConfig, LocalCodingAgent, OllamaClient
from local_coder_agent.voice import SpeechIO


class TestLocalAgentConfig(unittest.TestCase):
    def test_default_models_are_local_and_code_oriented(self):
        config = AgentConfig()
        self.assertEqual(config.planner_model, "hermes3")
        self.assertEqual(config.coder_model, "qwen2.5-coder")

    def test_agent_can_build_task_result_without_live_model(self):
        agent = LocalCodingAgent()
        result = agent.execute_task("List the top three steps for a local computer repair task.")
        self.assertIn("plan", result)
        self.assertIn("code", result)

    def test_ollama_client_uses_local_runtime_endpoint(self):
        client = OllamaClient()
        self.assertIn("localhost:11434", client.config.api_base)

    def test_voice_defaults_are_local_first(self):
        voice = SpeechIO()
        self.assertEqual(voice.dictation_backend, "vosk")
        self.assertIn("espeak-ng", voice.tts_command)

    def test_voxtype_alias_maps_to_local_backend(self):
        voice = SpeechIO(dictation_backend="voxtype")
        self.assertEqual(voice.dictation_backend, "vosk")


if __name__ == "__main__":
    unittest.main()
