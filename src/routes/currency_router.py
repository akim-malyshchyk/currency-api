from aiohttp.web import Application
from controllers.currency_controller import CurrencyController


def currency_routes(app: Application) -> None:
    controller = CurrencyController()
    app.router.add_get('/price/{currency:[A-Z]+}', controller.get_currency_price)
    app.router.add_get('/price/history', controller.get_history)
    app.router.add_delete('/price/history', controller.delete_history)
