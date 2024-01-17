from aiohttp import web
import pytest
from src.controllers import controller


@pytest.fixture
def cli(event_loop, aiohttp_client):
    app = web.Application()
    app.router.add_get('/', controller.index)
    return event_loop.run_until_complete(aiohttp_client(app))


async def test_set_value(cli):
    resp = await cli.get('/')
    assert resp.status == 200
    assert await resp.text() == 'This is root page'
