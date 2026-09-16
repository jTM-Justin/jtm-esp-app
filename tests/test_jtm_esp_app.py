import unittest

from jtm_esp_app.bridge import TunnelConfig, build_status
from jtm_esp_app.keyboard import KeyboardBuffer, KeyboardEvent


class TestJTMESPApp(unittest.TestCase):
    def test_tunnel_config_builds_https_url(self):
        config = TunnelConfig(tunnel_name="demo", hostname="demo.example.com", secure=True)
        self.assertEqual(config.url, "https://demo.example.com")

    def test_status_reports_secure_ready_state(self):
        status = build_status("demo", "demo.example.com", secure=True)
        self.assertEqual(status["status"], "ready")
        self.assertTrue(status["secure"])
        self.assertEqual(status["url"], "https://demo.example.com")

    def test_keyboard_buffer_tracks_active_key_text(self):
        buffer = KeyboardBuffer()
        buffer.record(KeyboardEvent("H", True))
        buffer.record(KeyboardEvent("i", True))
        buffer.record(KeyboardEvent("!", True))
        self.assertEqual(buffer.active_keys(), ["h", "i", "!"])
        self.assertEqual(buffer.text(), "hi!")

    def test_keyboard_buffer_releases_release_events(self):
        buffer = KeyboardBuffer()
        buffer.record(KeyboardEvent("A", True))
        buffer.record(KeyboardEvent("A", False))
        self.assertEqual(buffer.active_keys(), ["a"])
        self.assertEqual(buffer.text(), "a")
