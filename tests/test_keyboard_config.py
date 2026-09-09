import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / 'src' / 'config.h'
LAST = ROOT / 'src' / 'last_config.h'


class TestKeyboardConfig(unittest.TestCase):
    def test_target_endpoint_is_set(self):
        for name in (CONFIG, LAST):
            content = name.read_text(encoding='utf-8')
            self.assertIn('192.168.1.100', content)
            self.assertIn('8080', content)
            self.assertIn('/keyboard', content)

    def test_board_uses_fixed_local_ip(self):
        for name in (CONFIG, LAST):
            content = name.read_text(encoding='utf-8')
            self.assertIn('ESP32S3_KEYBOARD_LOCAL_IP "192.168.1.50"', content)
            self.assertIn('ESP32S3_KEYBOARD_GATEWAY "192.168.1.1"', content)
            self.assertIn('ESP32S3_KEYBOARD_SUBNET "255.255.255.0"', content)

    def test_board_has_no_display_audio_peripherals(self):
        for name in (CONFIG, LAST):
            content = name.read_text(encoding='utf-8')
            self.assertIn('#define ESP32S3_BOARD_HAS_DISPLAY 0', content)
            self.assertIn('#define ESP32S3_BOARD_HAS_MIC 0', content)
            self.assertIn('#define ESP32S3_BOARD_HAS_SPEAKER 0', content)

    def test_project_is_keyboard_only(self):
        content = CONFIG.read_text(encoding='utf-8')
        self.assertIn('USB_KEYBOARD_ONLY', content)


if __name__ == '__main__':
    unittest.main()
