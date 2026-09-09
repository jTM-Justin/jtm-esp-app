import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / 'src' / 'config.h'


class TestBridgeConfig(unittest.TestCase):
    def test_target_ip_and_port_are_configured(self):
        content = CONFIG.read_text(encoding='utf-8')
        self.assertIn('192.168.1.100', content)
        self.assertIn('8080', content)

    def test_device_has_two_usb_ports(self):
        content = CONFIG.read_text(encoding='utf-8')
        self.assertIn('2', content)

    def test_bridge_route_is_defined(self):
        content = CONFIG.read_text(encoding='utf-8')
        self.assertRegex(content, r'/bridge')


if __name__ == '__main__':
    unittest.main()
