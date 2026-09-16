import unittest

from local_coder_agent.agent import AgentConfig, LocalCodingAgent, OllamaClient


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


if __name__ == "__main__":
    unittest.main()
