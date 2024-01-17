from controllers import controller

def routes(app):
    app.router.add_get('/', controller.index)
