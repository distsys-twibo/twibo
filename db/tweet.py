import asyncio
import logging

import pymongo

from db.db_utils import db
from db import user_follow


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


async def create(user_id, tweet_id, content, timestamp):
    logger.debug('{} {} {}'.format(user_id, tweet_id, timestamp))
    await coll.insert_one({
        'user_id': user_id,
        'tweet_id': tweet_id,
        'content': content,
        'ts': timestamp
    })
    return 0


async def get(user_id, limit=50):
    '''get @user_id's @limit tweets'''
    logger.debug('user {} limit {}'.format(user_id, limit))
    cursor = coll.find(
        {'user_id': user_id},
        {'_id': False},
        limit=limit,
        sort=[('ts', pymongo.DESCENDING)])
    tweets = [t async for t in cursor]
    return tweets
