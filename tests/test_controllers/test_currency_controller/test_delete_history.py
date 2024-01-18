import pytest
from unittest.mock import AsyncMock
from aiohttp import web
from src.controllers.currency_controller import CurrencyController


@pytest.fixture
def mocks(mocker):
    mock_currency_manager = AsyncMock()
    mocker.patch('src.controllers.currency_controller.CurrencyDBManager', return_value=mock_currency_manager)
    
    return {
        'currency_manager': mock_currency_manager,
    }


@pytest.fixture
def cli(event_loop, aiohttp_client, mocks):
    app = web.Application()
    controller = CurrencyController()
    app.router.add_delete('/price/history', controller.delete_history)
    return event_loop.run_until_complete(aiohttp_client(app))


async def test_delete_history_success(cli, mocks):
    mocks['currency_manager'].delete_history.return_value = None

    response = await cli.delete("/price/history")

    assert response.status == 204
    assert await response.json() is None
