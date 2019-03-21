import asyncio
import logging

import pymongo

from utils.config import conf
from db.db_utils import db
from db import user_follow
from feeding import feeders

logger = logging.getLogger(__name__)

coll = db['tweet']
asyncio.gather(
    coll.create_index([
        ('user_id', pymongo.ASCENDING),
        ('ts', pymongo.DESCENDING)
    ]),
    coll.create_index([
        ('tweet_id', pymongo.ASCENDING),
        ('ts', pymongo.DESCENDING)
    ])
)

feeder = feeders.get(conf['feeder'], None)
logger.info('feeder is {}'.format(feeder))



async def create(user_id, tweet_id, content, timestamp):
    logger.debug('{} {} {}'.format(user_id, tweet_id, timestamp))
    await coll.insert_one({
        'user_id': user_id,
        'tweet_id': tweet_id,
        'content': content,
        'ts': timestamp
    })
    if feeder:
        await feeder.create(user_id, tweet_id, timestamp)
    return 0


async def _get_naive(user_id, limit):
    followees = await user_follow.all_followees(user_id)
    logger.debug('followees of {}: {}'.format(user_id, followees))
    query = {
        'user_id': {'$in': followees}
    }
    cursor = coll.find(query, {'_id': False}, limit=limit, sort=[('ts', pymongo.DESCENDING)])
    tweets = [t async for t in cursor]
    return tweets


async def _get_feeder(user_id, limit):
    feeds = await feeder.get(user_id, limit)
    logger.debug('{} found {} tweets'.format(user_id, len(feeds)))
    tids = [f[0] for f in feeds]
    cursor = coll.find({'tweet_id': {'$in': tids}}, {'_id': False})
    tweets = [t async for t in cursor]
    return tweets


async def get(user_id, limit=50):
    '''user want @limit tweets'''
    logger.debug('user {} limit {}'.format(user_id, limit))
    if feeder:
        return await _get_feeder(user_id, limit)
    return await _get_naive(user_id, limit)
