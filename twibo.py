import argparse
import logging

from aiohttp import web

import background
from caching import caching_utils
from db import db_utils
from utils import config


logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s:%(asctime)s:%(name)s:%(lineno)d:%(funcName)s - %(message)s')


parser = argparse.ArgumentParser(description="aiohttp server example")
parser.add_argument('--path', default=None)
parser.add_argument('--port', default=None)


if __name__ == '__main__':
    config.init()
    caching_utils.init_cache(config.conf)
    db_utils.init_db(config.conf)
    import views

    app = web.Application()
    app.add_routes([
        web.get('/', views.index.hello),
        *views.tweet.routes,
        *views.user.routes
    ])

    app.on_startup.append(background.add_tasks)

    args = parser.parse_args()
    web.run_app(app, path=args.path, port=args.port)
