import argparse
import logging

from aiohttp import web

from utils import config
from db import db_utils


logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s:%(asctime)s:%(name)s:%(lineno)d:%(funcName)s - %(message)s')


parser = argparse.ArgumentParser(description="aiohttp server example")
parser.add_argument('--path', default=None)
parser.add_argument('--port', default=9990)


if __name__ == '__main__':
    config.init()
    db_utils.init_db(config.conf)
    import views

    app = web.Application()
    app.add_routes([
        web.get('/', views.index.hello),
        *views.tweet.routes,
        *views.user.routes
    ])

    args = parser.parse_args()
    web.run_app(app, path=args.path, port=args.port)
