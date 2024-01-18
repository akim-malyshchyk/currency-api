from aiohttp import web
import pytest
from src.controllers.currency_controller import CurrencyController


@pytest.fixture
def cli(event_loop, aiohttp_client):
    app = web.Application()
    controller = CurrencyController()
    app.router.add_get('/price/{currency}', controller.get_currency_price)
    app.router.add_get('/history', controller.get_history)
    app.router.add_delete('/price/history', controller.delete_history)
    return event_loop.run_until_complete(aiohttp_client(app))


def test_get_price(cli):
    pass


def test_get_history(cli):
    pass


def test_delete_history(cli):
    pass
