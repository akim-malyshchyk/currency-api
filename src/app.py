from aiohttp import web
from src.core.router import routes


async def factory():
    app = web.Application()
    routes(app)
    return app
