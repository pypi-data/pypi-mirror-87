import ipaddress
import re
from IPy import IP


class IpUtils(object):
    VALID_IPV4_PATTERN = re.compile("(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.){3}([01]?\\d\\d?|2[0-4]\\d|25[0-5])")
    VALID_IPV6_PATTERN = re.compile("([0-9a-f]{1,4}:){7}([0-9a-f]){1,4}")

    @staticmethod
    def is_ip_address(ip_address):
        if IpUtils.VALID_IPV4_PATTERN.match(ip_address):
            return True
        if IpUtils.VALID_IPV6_PATTERN.match(ip_address):
            return True
        return False

    @staticmethod
    def is_valid_public_ip(ip_address):
        ip = ipaddress.ip_address(ip_address)

        if ip.version is 4:
            if not ip.is_loopback and not ip.is_reserved and not ip.is_unspecified and IP(ip_address).iptype() is not "PRIVATE":
                return True
            return False

        if not ip.is_unspecified and IP(ip_address).iptype() is not "PRIVATE":
            return True
        return False

    @staticmethod
    def is_loop_back(ip_address):
        return ipaddress.IPv4Address(ip_address).is_loopback
