import ipaddress
import re


def is_valid_ipv4_address(address):
    try:
        ipaddress.IPv4Address(address)
        return True
    except ipaddress.AddressValueError:
        return False


def is_valid_mac_address(address):
    pattern = r'^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$'
    return re.match(pattern, address) is not None
