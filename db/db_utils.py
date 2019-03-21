import asyncio
import logging

import aioredis
import motor.motor_asyncio


logger = logging.getLogger(__name__)

db = None
db_r = None


def init_db(conf):
    global db, db_r
    host = host = conf['mongo-host']
    port = conf['mongo-port']
    mdb = conf['mongo-db']
    logger.debug('initializing db(mongo): {} {} {}'.format(host, port, mdb))
    db = motor.motor_asyncio.AsyncIOMotorClient(host, port)[mdb]

    host = host = conf['redis-host']
    port = conf['redis-port']
    rdb = conf['redis-db']
    logger.debug('initializing db(redis): {} {} {}'.format(host, port, rdb))
    # don't know why yet but must run like this before running aiohttp
    loop = asyncio.get_event_loop()
    db_r = loop.run_until_complete(aioredis.create_redis_pool((host, port), db=rdb, maxsize=50))


async def exists(coll, query):
    try:
        await coll.find_one(query)
    except:
        return False
    return True
