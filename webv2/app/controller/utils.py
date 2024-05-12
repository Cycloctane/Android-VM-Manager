import re

def is_mac_address(addr: str) -> bool:
    mac_pattern = r"^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$"
    return False if re.match(mac_pattern, addr) is None else True
