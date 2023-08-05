import unittest

from securenative.utils.ip_utils import IpUtils


class IpUtilTest(unittest.TestCase):

    def test_is_ip_address_valid_ipv4(self):
        valid_ipv4 = "172.16.254.1"
        self.assertTrue(IpUtils.is_ip_address(valid_ipv4))

    def test_is_ip_address_valid_ipv6(self):
        valid_ipv6 = "2001:db8:1234:0000:0000:0000:0000:0000"
        self.assertTrue(IpUtils.is_ip_address(valid_ipv6))

    def test_is_ip_address_invalid_ipv4(self):
        invalid_ipv4 = "172.16.2541"
        self.assertFalse(IpUtils.is_ip_address(invalid_ipv4))

    def test_is_ip_address_invalid_ipv6(self):
        invalid_ipv6 = "2001:db8:1234:0000"
        self.assertFalse(IpUtils.is_ip_address(invalid_ipv6))

    def test_is_valid_public_ip(self):
        ip = "64.71.222.37"
        self.assertTrue(IpUtils.is_valid_public_ip(ip))

    def test_is_not_valid_public_ip(self):
        ip = "10.0.0.0"
        self.assertFalse(IpUtils.is_valid_public_ip(ip))

    def test_is_valid_loopback_ip(self):
        ip = "127.0.0.1"
        self.assertTrue(IpUtils.is_loop_back(ip))
