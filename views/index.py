from datetime import datetime

from aiohttp import web


async def hello(request):
    return web.Response(text='Hello, now is {}'.format(datetime.now()))
