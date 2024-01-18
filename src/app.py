from aiohttp import web
from routes.currency_router import currency_routes


async def factory():
    app = web.Application()
    currency_routes(app)
    return app
