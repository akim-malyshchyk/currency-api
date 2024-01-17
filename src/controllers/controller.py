from views import render

async def index(request):
    data = "This is root page"
    return await render.raw(data, status=200)
