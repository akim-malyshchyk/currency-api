from aiohttp import web
from core.router import routes


async def factory():
    app = web.Application()
    routes(app)
    return app
