import asyncio
import logging

import aioredis
import motor.motor_asyncio


logger = logging.getLogger(__name__)

db = None


def init_db(conf):
    global db
    host = conf['mongo-host']
    port = conf['mongo-port']
    mdb = conf['mongo-db']
    logger.debug('initializing db(mongo): {} {} {}'.format(host, port, mdb))
    db = motor.motor_asyncio.AsyncIOMotorClient(host, port)[mdb]


async def exists(coll, query):
    try:
        await coll.find_one(query)
    except:
        return False
    return True
