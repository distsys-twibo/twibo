import asyncio
import logging
import time

from caching.caching_utils import redis
from db import tweet, user_follow
from utils.config import conf
from .base_feeder import BaseFeeder

logger = logging.getLogger(__name__)


class FeedPush(BaseFeeder):
    """
    Every user has a list of feeds waiting to be read/retrieved.
    When creating, create the tweet in db, and push the tweet_id to all followers' feed lists
    When getting, retrieve tweet_ids from the user's feed list, and read tweets from db
    """
    prefix = 'feedpush'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create(self, user_id, tweet_id, content, timestamp, **kwargs):
        logger.debug('user_id {} tweet_id {} ts {}'.format(
            user_id, tweet_id, timestamp))
        followers = await user_follow.all_followers(user_id)
        t_db = tweet.create(user_id, tweet_id, content, timestamp)
        # add tweet id to the feed list of all followers
        t_feedlist = (redis.zadd(self.get_key(flr), timestamp, tweet_id)
                      for flr in followers)
        await asyncio.gather(t_db, *t_feedlist)
        return 0

    async def get(self, user_id, limit, **kwargs):
        # get the ids of latest @limit tweets from the user's feed list
        pop = kwargs.get('pop', False)
        k = self.get_key(user_id)
        logger.debug('user_id {} limit {} redis key {} pop {}'.format(user_id, limit, k, pop))
        if pop:
            tweet_ids = await redis.execute(b'ZPOPMAX', k, limit, encoding='utf8')
        else:
            tweet_ids = await redis.zrevrange(self.get_key(user_id), 0, limit - 1, encoding='utf8')
        tweets = await tweet.get_by_tweet_ids(tweet_ids)
        tweets.sort(key=lambda x: x['ts'], reverse=True)
        return tweets


class FeedPushCacheAside(FeedPush):
    """
    Creating a tweet is the same as FeedPush, i.e. write to db.
    When reading, first retrieve tweet_ids from feed list.
    Then first find the tweets in a global cache of tweets (tweet_id -> tweet).
    if not found, find from db, and insert to cache.
    Need to set expire interval; add a parameter in config.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix_cache = 'feedpush-cache'  # global cache
        self.expire_interval = conf['cache-expire-interval']

    async def get(self, user_id, limit, **kwargs):
        pop = kwargs.get('pop', False)
        k = self.get_key(user_id)
        logger.debug('user_id {} limit {} redis key {} pop {}'.format(user_id, limit, k, pop))
        if pop:
            tweet_ids = await redis.execute(b'ZPOPMAX', k, limit, encoding='utf8')
        else:
            tweet_ids = await redis.zrevrange(self.get_key(user_id), 0, limit - 1, encoding='utf8')
        # check if the tweets exist in cache
        tweets = await redis.exists(tweet_ids)
        if tweets == 0:
            tweets = await tweet.get_by_tweet_ids(tweet_ids)
            tweets.sort(key=lambda x: x['ts'], reverse=True)
            await redis.lpush(tweet_ids, *tweets)
            await redis.expire(tweet_ids, self.expire_interval)
        tweets = await redis.lrange(tweet_ids, 0, limit)
        return tweets


class FeedPushWriteBehind(FeedPushCacheAside):
    """
    Getting tweets is the same as FeedPushCacheAside.
    Creating tweets writes to the same global cache FeedPushCacheAside uses,
    and also write to a sorted set (zset) so we get to know which tweets
    are written to db.
    A worker runs in the background which flushes new data to db periodically.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix_track = 'feedpush-track'
        expire = conf['cache-expire-interval']
        interval = conf['write-behind-interval']
        assert interval * 2 < expire, 'cache-expire-interval must be at least 2 times greater than ' \
                                      'write-behind-interval '
        logger.debug('launching write-behind worker with interval {}'.format(interval))
        loop = asyncio.get_event_loop()
        loop.create_task(self._persistence_worker(interval))

    async def _persistence_worker(self, interval):
        t0 = time.time()
        while 1:
            now = time.time()
            elapsed = now - t0
            if elapsed <= interval:
                await asyncio.sleep(interval - elapsed)
            t0 = now
            logger.debug('write behind worker running')

    async def create(self, user_id, tweet_id, content, timestamp, **kwargs):
        """
        only write to cache
        let background worker flush them to db
        """
        logger.debug('user_id {} tweet_id {} ts {}'.format(
            user_id, tweet_id, timestamp))
        followers = await user_follow.all_followers(user_id)
        # add tweet id to the feed list of all followers
        t_feedlist = (redis.zadd(self.get_key(flr), timestamp, tweet_id)
                      for flr in followers)
        await asyncio.gather(t_feedlist)
        return 0
