from aiohttp import web
import pytest
from src.controllers import controller


@pytest.fixture
def cli(event_loop, aiohttp_client):
    app = web.Application()
    app.router.add_get('/', controller.index)
    return event_loop.run_until_complete(aiohttp_client(app))

