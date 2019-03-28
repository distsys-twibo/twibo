import asyncio
import logging

import aioredis


logger = logging.getLogger(__name__)

redis = None


def init_cache(conf):
    global redis
    host = conf['redis-host']
    port = conf['redis-port']
    rdb = conf['redis-db']
    logger.warn('initializing cache(redis): {} {} {}'.format(host, port, rdb))
    # don't know why yet but must run like this before running aiohttp
    loop = asyncio.get_event_loop()
    redis = loop.run_until_complete(aioredis.create_redis_pool((host, port), db=rdb, maxsize=50))
