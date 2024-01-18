from typing import Any, Optional
from aiohttp import web
from aiohttp.typedefs import LooseHeaders


async def json(data: Any, status: int, headers: Optional[LooseHeaders] = None) -> web.Response:
    response = web.json_response(data, status=status, headers=headers, content_type='application/json')
    return response


async def raw(data: Any, status: int, headers: Optional[LooseHeaders] = None) -> web.Response:
    response = web.Response(text=data, status=status, headers=headers, content_type='text/plain')
    return response
