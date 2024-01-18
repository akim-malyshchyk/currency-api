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
    app.router.add_get('/price/history', controller.get_history)
    return event_loop.run_until_complete(aiohttp_client(app))


async def test_get_history_success(cli, mocks):
    currency_data = {'mocked_response': 'success'}
    mocks['currency_manager'].get_history.return_value = currency_data

    response = await cli.get("/price/history?page=1")

    assert response.status == 200
    assert await response.json() == currency_data


async def test_get_history_without_page_success(cli, mocks):
    currency_data = {'mocked_response': 'success'}
    mocks['currency_manager'].get_history.return_value = currency_data

    response = await cli.get("/price/history")

    assert response.status == 200
    assert await response.json() == currency_data


async def test_get_history_bad_request(cli, mocks):
    response = await cli.get("/price/history?page=not-a-number")

    assert response.status == 400
    assert 'Invalid page number' in await response.text()
