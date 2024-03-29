import os
import ccxt.async_support as ccxt
from aiohttp.web import (
    HTTPBadRequest,
    Request,
    Response,
)
from managers.currency_db_manager import CurrencyDBManager
from helpers import render


class CurrencyController:
    def __init__(self):
        self.exchange_config = {
            "enableRateLimit": True,
            "apiKey": os.getenv("KUCOIN_API_KEY"),
            "secret": os.getenv("KUCION_API_SECRET")
        }
        self.currency_manager = CurrencyDBManager()

    async def get_currency_price(self, request: Request) -> Response:
        currency = request.match_info["currency"]
        symbol = f"{currency}/USDT"
        exchange = ccxt.kucoin(self.exchange_config)
        try:
            ticker = await exchange.fetch_ticker(symbol)
        except ccxt.BadSymbol as err:
            raise HTTPBadRequest(text=str(err)) from err
        finally:
            await exchange.close()

        last_price = ticker['last']
        data = await self.currency_manager.save_currency(currency, last_price)

        return await render.json(
            data=data,
            status=200
        )

    async def get_history(self, request: Request) -> Response:
        try:
            page = int(request.query.get("page", "1"))
        except ValueError as err:
            raise HTTPBadRequest(text="Invalid page number") from err

        data = await self.currency_manager.get_history(page)
        return await render.json(data, status=200)

    async def delete_history(self, request: Request) -> Response:  # pylint: disable=unused-argument
        await self.currency_manager.delete_history()
        return await render.json(data=None, status=204)
