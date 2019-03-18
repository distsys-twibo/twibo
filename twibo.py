from aiohttp import web

from views import index


app = web.Application()
app.add_routes([
    web.get('/', index.hello)
])

web.run_app(app)
