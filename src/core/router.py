from aiohttp.web import Application
from controllers.controller import Controller


def routes(app: Application) -> None:
    controller = Controller()
    app.router.add_get('/price/{currency}', controller.get_currency_price)
    app.router.add_get('/history', controller.get_history)
    app.router.add_delete('/price/history', controller.delete_history)
