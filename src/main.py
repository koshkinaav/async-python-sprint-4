# import sys
# import logging
#
# from tortoise import Tortoise, run_async, functions
# from models.models import ShortUrl
#
# # Для отображения SQL-запросов в консоли настроим логирование
# fmt = logging.Formatter(
#     fmt="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
# )
# sh = logging.StreamHandler(sys.stdout)
# sh.setLevel(logging.DEBUG)
# sh.setFormatter(fmt)
#
# logger_db_client = logging.getLogger("db_client")
# logger_db_client.setLevel(logging.DEBUG)
# logger_db_client.addHandler(sh)
#
#
# async def main():
#
#     DSN = "postgres://alex:xxx@localhost:5432/short_urls"
#     await Tortoise.init(
#         db_url=DSN,
#         modules={'models': ['models.models']}
#     )
#     await Tortoise.generate_schemas()
#     url = await ShortUrl.get(id=short_url.id)
#     print(url)
#
# run_async(main())
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
from core import config
from core.logger import LOGGING
from api.v1 import base

app = FastAPI(
    # Конфигурируем название проекта. Оно будет отображаться в документации
    title=config.PROJECT_NAME,
    # Адрес документации в красивом интерфейсе
    docs_url='/api/openapi',
    # Адрес документации в формате OpenAPI
    openapi_url='/api/openapi.json',
    # Можно сразу сделать небольшую оптимизацию сервиса
    # и заменить стандартный JSON-сериализатор на более шуструю версию, написанную на Rust
    default_response_class=ORJSONResponse,
)

app.include_router(base.router, prefix='/api/v1')

register_tortoise(
    app,
    db_url="postgres://alex:xxx@localhost:5432/short_urls",
    modules={"models": ["src.models.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == '__main__':
    # Приложение может запускаться командой
    # `uvicorn main:app --host 0.0.0.0 --port 8080`
    # но чтобы не терять возможность использовать дебагер,
    # запустим uvicorn сервер через python
    uvicorn.run(
        'main:app',
        host=config.PROJECT_HOST,
        port=config.PROJECT_PORT,
    )
