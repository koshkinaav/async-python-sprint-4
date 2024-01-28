from src.models.models import ShortUrl


async def check_short_url_exists(short_url):
    count = await ShortUrl.filter(short_url=short_url).count()
    return count > 0


async def check_url_exists(url):
    count = await ShortUrl.filter(url=url).count()
    return count > 0
