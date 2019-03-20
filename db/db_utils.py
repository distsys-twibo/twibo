import logging

from redis import Redis
from pymongo import MongoClient


logger = logging.getLogger(__name__)

db = None
db_r = None


def init_db(conf):
    global db, db_r
    host = host = conf['mongo-host']
    port = conf['mongo-port']
    mdb = conf['mongo-db']
    logger.debug('initializing db(mongo): {} {} {}'.format(host, port, mdb))
    db = MongoClient(host, port)[mdb]

    host = host = conf['redis-host']
    port = conf['redis-port']
    rdb = conf['redis-db']
    logger.debug('initializing db(redis): {} {} {}'.format(host, port, rdb))
    db_r = Redis(host=host, port=port, db=rdb)


def exists(coll, query):
    try:
        coll.find_one(query)
    except:
        return False
    return True
