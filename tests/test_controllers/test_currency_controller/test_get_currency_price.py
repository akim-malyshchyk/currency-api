import ccxt
import pytest
from unittest.mock import AsyncMock
from aiohttp import web
from src.controllers.currency_controller import CurrencyController


@pytest.fixture
def mocks(mocker):
    mock_exchange = AsyncMock()
    mock_currency_manager = AsyncMock()
    
    mocker.patch('src.controllers.currency_controller.ccxt.kucoin', return_value=mock_exchange)
    mocker.patch('src.controllers.currency_controller.CurrencyDBManager', return_value=mock_currency_manager)

    return {
        'currency_manager': mock_currency_manager,
        'exchange': mock_exchange
    }


@pytest.fixture
def cli(event_loop, aiohttp_client, mocks):
    app = web.Application()
    controller = CurrencyController()
    app.router.add_get('/price/{currency:[A-Z]+}', controller.get_currency_price)
    return event_loop.run_until_complete(aiohttp_client(app))


async def test_get_currency_price_success(cli, mocks):
    ticker_data = {'last': 123.45}
    currency_data = {'mocked_response': 'success'}
    mocks['exchange'].fetch_ticker.return_value = ticker_data
    mocks['currency_manager'].save_currency.return_value = currency_data

    response = await cli.get("/price/BTC")

    assert response.status == 200
    assert await response.json() == currency_data


async def test_get_currency_price_bad_request(cli, mocks):
    mocks['exchange'].fetch_ticker.side_effect = ccxt.BadSymbol('Invalid symbol')

    response = await cli.get("/price/INVALID")

    assert response.status == 400
    assert 'Invalid symbol' in await response.text()
