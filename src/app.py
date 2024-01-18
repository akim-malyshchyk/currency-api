import logging
import os
from aiohttp import web
from aiohttp_middlewares import (
    cors_middleware,
    error_middleware,
    https_middleware,
)
from aiohttp_middlewares.cors import DEFAULT_ALLOW_HEADERS
from routes.currency_router import currency_routes


async def factory():
    app = web.Application(middlewares=[
        error_middleware(
            ignore_exceptions=web.HTTPNotFound,
        ),
        cors_middleware(
            origins=[os.getenv("API_URL", "*")],
            allow_methods=("GET", "DELETE"),
            allow_headers=DEFAULT_ALLOW_HEADERS,
        ),
        https_middleware(),
    ])
    logging.basicConfig(level=logging.INFO)
    currency_routes(app)
    return app
