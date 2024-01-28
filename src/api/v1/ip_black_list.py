blacklist = [
    "192.168.1.0/24",
    "0.0.0.0",
]


async def is_ip_in_black_list(ip: str) -> bool:
    if ip in blacklist:
        return True
    else:
        return False
