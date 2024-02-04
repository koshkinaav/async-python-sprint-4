blacklist = [
# Напишите здесь список запрщенных ip
]


async def is_ip_in_black_list(ip: str) -> bool:
    if ip in blacklist:
        return True
    else:
        return False
