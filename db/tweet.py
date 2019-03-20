import logging

import pymongo

from db.db_utils import db
from db import user_follow
# from feeding.feed_pull import fp

logger = logging.getLogger(__name__)

coll = db['tweet']
feeder = None

coll.create_index()


def create(user_id, tweet_id, content, timestamp):
    logger.debug('{} {} {}'.format(user_id, tweet_id, timestamp))
    coll.insert_one({
        'user_id': user_id,
        'tweet_id': tweet_id,
        'content': content,
        'ts': timestamp
    })
    if feeder:
        feeder.create(user_id, tweet_id, timestamp)
    return 0


def _get_naive(user_id, limit):
    followees = list(user_follow.all_followees(user_id))
    logger.debug('followees of {}: {}'.format(user_id, followees))
    query = {
        'user_id': {'$in': followees}
    }
    tweets = coll.find(query, limit=limit, sort=[('ts', pymongo.DESCENDING)])
    return list(tweets)


def _get_feeder(user_id, limit):
    feeds = feeder.get(user_id, limit)
    logger.debug('{} found {} tweets'.format(user_id, len(feeds)))
    tids = [f[0] for f in feeds]
    tweets = coll.find({'tweet_id': {'$in': tids}})
    return list(tweets)


def get(user_id, limit=50):
    '''user want @limit tweets'''
    logger.debug('user {} limit {}'.format(user_id, limit))
    if feeder:
        return _get_feeder(user_id, limit)
    return _get_naive(user_id, limit)
