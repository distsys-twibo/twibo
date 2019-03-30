import asyncio
import logging

import aioredis


logger = logging.getLogger(__name__)

# redis is for storing feed lists
# redis_lru is for tweet contents which can be LRU'ed
redis = None
redis_lru = None


def init_cache(conf):
    global redis, redis_lru
    host = conf['redis-host']
    port = conf['redis-port']
    rdb = conf['redis-db']
    logger.warn('initializing cache(redis): {} {} {}'.format(host, port, rdb))
    # don't know why yet but must run like this before running aiohttp
    loop = asyncio.get_event_loop()
    redis = loop.run_until_complete(aioredis.create_redis_pool((host, port), db=rdb, maxsize=50))

    host = conf['redis-lru-host']
    port = conf['redis-lru-port']
    rdb = conf['redis-lru-db']
    logger.warn('initializing cache(redis-lru): {} {} {}'.format(host, port, rdb))
    # don't know why yet but must run like this before running aiohttp
    loop = asyncio.get_event_loop()
    redis_lru = loop.run_until_complete(aioredis.create_redis_pool((host, port), db=rdb, maxsize=50))
