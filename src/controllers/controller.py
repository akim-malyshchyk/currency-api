from src.views import render

async def index(request):  # pylint: disable=unused-argument
    data = "This is root page"
    return await render.raw(data, status=200)
