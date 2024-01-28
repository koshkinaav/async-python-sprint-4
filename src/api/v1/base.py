import logging
from datetime import datetime
from typing import List
from fastapi import APIRouter, status, HTTPException, Depends, FastAPI
from src.models.models import ShortUrl
from src.services.generate_short_url import generate_short_url
from src.services.check import check_short_url_exists, check_url_exists
from fastapi.responses import RedirectResponse
from fastapi.requests import Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from src.api.v1.ip_black_list import is_ip_in_black_list
router = APIRouter()


@router.get("/ping")
async def ping_db():
    try:
        await ShortUrl.filter().first()
        return {"status": "Database is accessible"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post('/url', status_code=status.HTTP_201_CREATED)
async def create_shorturl(request: Request, url: str):
    ip = request.client.host
    if not is_ip_in_black_list(ip):
        try:
            url_already_exists = await check_url_exists(url)
            if not url_already_exists:
                short_url = ShortUrl(url=url, short_url=generate_short_url(url))
                await short_url.save()
                return {
                    'short_url': f'http://localhost:8000/api/v1/{short_url.short_url}'
                }
            else:
                return await ShortUrl.filter(url=url).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    else:
        return HTTPException(status_code=403, detail='Permission Denied')


@router.post('/batch_urls', status_code=status.HTTP_201_CREATED)
async def create_shorturls(urls: List[str]):
    short_urls = []

    for url in urls:
        if not check_short_url_exists(url):
            short_url = ShortUrl(url=url, short_url=generate_short_url(url))
            await short_url.save()
            short_urls.append(f'http://localhost:8000/api/v1/{short_url.short_url}')
        else:
            return HTTPException(status_code=409, detail=f"URL {url} already exists")

    return short_urls


@router.get('/shorten-url-id', status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def get_url(short_url: str):
    short_url = short_url.split("/")[-1]
    short_url_obj = await ShortUrl.filter(short_url=short_url).first()

    if short_url_obj:
        return {
            'location': short_url_obj.url,
            'redirect_count': short_url_obj.redirect_count
        }
    else:
        return {
            'error': 'Short URL not found'
        }


@router.get("/{short_url}/status")
async def status(request: Request, short_url: str):
    flg = await check_short_url_exists(short_url=short_url)
    if flg:
        url = await ShortUrl.filter(short_url=short_url).first()
        redirect_count = url.redirect_count
        client_ip = request.client.host
        return {
            'short_url': f'http://localhost:8000/api/v1/{short_url}',
            'redirect_count': redirect_count,
            'last_client_ip': client_ip
        }
    else:
        raise HTTPException(status_code=404, detail="Short URL not found")


@router.get("/{short_url}")
async def redirect_to_original(short_url: str):
    flg = await check_short_url_exists(short_url=short_url)
    if flg:
        url = await ShortUrl.filter(short_url=short_url).first()
        url.last_redirected_date = datetime.now()
        url.redirect_count += 1
        await url.save()
        return RedirectResponse(url=url.url)
    else:
        raise HTTPException(status_code=404, detail="Short URL not found")
