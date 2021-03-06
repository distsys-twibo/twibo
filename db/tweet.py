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


async def create_many(tweets):
    return await coll.insert_many(tweets)


async def create(user_id, tweet_id, content, timestamp):
    await coll.insert_one({
        'user_id': user_id,
        'tweet_id': tweet_id,
        'content': content,
        'ts': timestamp
    })
    return 0


async def get(query, **kwargs):
    cursor = coll.find(query, {'_id': False}, **kwargs)
    tweets = [t async for t in cursor]
    return tweets

def get_by_user_ids(user_ids, limit=50):
    return get(
        {'user_id': {'$in': user_ids}},
        limit=limit,
        sort=[('ts', pymongo.DESCENDING)]
    )

def get_by_user_id(user_id, limit=50):
    '''get @user_id's @limit tweets'''
    return get(
        {'user_id': user_id},
        limit=limit,
        sort=[('ts', pymongo.DESCENDING)]
    )


def get_by_tweet_ids(tweet_ids):
    return get({
        'tweet_id': {'$in': tweet_ids}
    })


def get_by_tweet_id(tweet_id):
    return get({
        'tweet_id': tweet_id
    })
