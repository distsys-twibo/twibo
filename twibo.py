import argparse
from aiohttp import web

from views import index


parser = argparse.ArgumentParser(description="aiohttp server example")
parser.add_argument('--path', default=None)
parser.add_argument('--port', default=None)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([
        web.get('/', index.hello)
    ])

    args = parser.parse_args()
    web.run_app(app, path=args.path, port=args.port)
