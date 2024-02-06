from datetime import datetime
from typing import List, Dict
from fastapi import APIRouter, status, HTTPException
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from src.api.v1.ip_black_list import is_ip_in_black_list
from src.models.models import ShortUrl
from src.services.check import check_short_url_exists, check_url_exists
from src.services.generate_short_url import generate_short_url
import logging
from src.core import config
from src.core.logger import LOGGING

router = APIRouter()


class StausItem(BaseModel):
    short_url: str
    redirect_count: int
    last_client_ip: str


class UrlItem(BaseModel):
    short_url: str | list


class ShortenUrlId(BaseModel):
    location: str
    redirect_count: int


@router.get("/api/v1/ping")
async def ping_db() -> dict:
    try:
        await ShortUrl.filter().first()
        logging.info('Trying to ping the database. Connection is successful.')
        return {"status": "Database is accessible"}
    except Exception as e:
        logging.exception('Could not ping the database. Connection is not successful.')
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post('/api/v1/url', status_code=status.HTTP_201_CREATED)
async def create_shorturl(request: Request, url: str) -> UrlItem:
    ip = request.client.host
    if is_ip_in_black_list(ip):
        HTTPException(status_code=403, detail='Permission Denied')
    else:
        try:
            url_already_exists = await check_url_exists(url)
            if not url_already_exists:
                short_url = ShortUrl(url=url, short_url=generate_short_url(url))
                await short_url.save()
                logging.info(f"Created shorturl: {short_url}")
                return UrlItem(short_url=f'http://localhost:8000/{short_url.short_url}')
            else:
                return await ShortUrl.filter(url=url).first()
        except Exception as e:
            logging.exception(f"Raised exception: {e}")
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.post('/api/v1/batch_urls', status_code=status.HTTP_201_CREATED)
async def create_shorturls(urls: List[str]) -> UrlItem:
    short_urls = []

    for url in urls:
        if await check_short_url_exists(url):
            logging.info(f"Trying to create existing url: {url}")
            return HTTPException(status_code=409, detail=f"URL {url} already exists")
    for url in urls:
        short_url = ShortUrl(url=url, short_url=generate_short_url(url))
        await short_url.save()
        logging.info(f"Created shorturl: {short_url}")
        short_urls.append(f'http://localhost:8000/{short_url.short_url}')

    return UrlItem(short_url=short_urls)


@router.get('/api/v1/shorten-url-id', status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def get_url(short_url: str) -> ShortenUrlId | dict[str, str]:
    short_url = short_url.split("/")[-1]
    short_url_obj = await ShortUrl.filter(short_url=short_url).first()

    if short_url_obj:
        return ShortenUrlId(location=short_url_obj.url, redirect_count=short_url_obj.redirect_count)
    else:
        return {
            'error': 'Short URL not found'
        }


@router.get("/api/v1/{short_url}/status")
async def status(request: Request, short_url: str) -> StausItem:
    flg = await check_short_url_exists(short_url=short_url)
    if flg:
        url = await ShortUrl.filter(short_url=short_url).first()
        redirect_count = url.redirect_count
        client_ip = request.client.host
        return StausItem(short_url=f'http://localhost:8000/{short_url}',
                         redirect_count=redirect_count,
                         client_ip=client_ip)
    else:
        logging.warning(f'Short URL {short_url} not found')
        raise HTTPException(status_code=404, detail="Short URL not found")


@router.get("/{short_url}")
async def redirect_to_original(short_url: str) -> RedirectResponse:
    flg = await check_short_url_exists(short_url=short_url)
    if flg:
        url = await ShortUrl.filter(short_url=short_url).first()
        url.last_redirected_date = datetime.now()
        url.redirect_count += 1
        await url.save()
        logging.info(f'Redirected to {url.url} successfully')
        return RedirectResponse(url=url.url)
    else:
        raise HTTPException(status_code=404, detail="Short URL not found")
