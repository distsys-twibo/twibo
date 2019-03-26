import asyncio
import logging
import heapq
import json
import random
import time

from caching.caching_utils import redis
from db import tweet, user_follow
from .base_feeder import BaseFeeder
from utils.config import conf


logger = logging.getLogger(__name__)


class FeedPush(BaseFeeder):
    '''
    Every user has a list of feeds waiting to be read/retrieved.
    When creating, create the tweet in db, and push the tweet_id to all followers' feed lists
    When getting, retrieve tweet_ids from the user's feed list, and read tweets from db
    '''
    prefix = 'feedpush'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name_feedlock = 'feed-lock'

    async def create(self, user_id, tweet_id, content, timestamp, **kwargs):
        logger.debug('user_id {} tweet_id {} ts {}'.format(
            user_id, tweet_id, timestamp))
        timer = kwargs.get('timer', {})
        t0 = time.time()
        followers = await user_follow.all_followers(user_id)
        t1 = time.time()
        t_db = tweet.create(user_id, tweet_id, content, timestamp)
        # add tweet id to the feed list of all followers
        # TODO: this lock is too big; maybe only set a per-user lock
        await self.lock(self.name_feedlock)
        t2 = time.time()
        t_feedlist = (redis.lpush(self.get_key(flr), tweet_id)
                        for flr in followers)
        await asyncio.gather(t_db, *t_feedlist)
        t3 = time.time()
        await self.unlock(self.name_feedlock)
        timer['db_get_follower'] = t1 - t0
        timer['op_lock'] = t2 - t1
        timer['other_create_and_push_feedlist'] = t3 - t2
        return 0

    async def get(self, user_id, limit, **kwargs):
        # get the ids of latest @limit tweets from the user's feed list
        pop = kwargs.get('pop', False)
        k = self.get_key(user_id)
        logger.debug('user_id {} limit {} redis key {} pop {}'.format(user_id, limit, k, pop))
        timer = kwargs.get('timer', {})
        t0 = time.time()
        if pop:
            await self.lock(self.name_feedlock)
        t1 = time.time()
        tweet_ids = await redis.lrange(k, 0, limit - 1, encoding='utf8')
        t2 = time.time()
        if pop:
            await redis.ltrim(k, len(tweet_ids), -1)
            await self.unlock(self.name_feedlock)
        t3 = time.time()
        tweets = await tweet.get_by_tweet_ids(tweet_ids)
        t4 = time.time()
        tweets.sort(key=lambda x: x['ts'], reverse=True)
        t5 = time.time()
        timer['op_lock'] = t1 - t0
        timer['cache_get_tweet_ids'] = t2 - t1
        timer['cache_pop_tweets'] = t3 - t2
        timer['db_get_tweet'] = t4 - t3
        timer['op_sort'] = t5 - t4
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
        timer = kwargs.get('timer', {})
        t0 = time.time()
        if pop:
            await self.lock(self.name_feedlock)
        t1 = time.time()
        tweet_ids = await redis.lrange(k, 0, limit - 1, encoding='utf8')
        t2 = time.time()
        if pop:
            await redis.ltrim(k, len(tweet_ids), -1)
            await self.unlock(self.name_feedlock)
        t3 = time.time()
        # check if the tweets exist in cache
        tweets = []
        n = len(tweet_ids)
        if n != 0:
            _tweet_ids = (self.get_key(self.prefix_cache, id) for id in tweet_ids)
            tweets = await redis.mget(*_tweet_ids)
        t4 = time.time()
        t_get_tweet = 0
        t_set_cache = 0
        for _index, each_t in enumerate(tweets):
            if not each_t:
                t_id = tweet_ids[_index]
                tt0 = time.time()
                t = await tweet.get_by_tweet_id(t_id)
                tt1 = time.time()
                json_t = json.dumps(t[0])
                await redis.set(self.get_key(self.prefix_cache, t_id), json_t, expire=self.expire_interval)
                tt2 = time.time()
                tweets[_index] = t[0]
                t_get_tweet += tt1 - tt0
                t_set_cache += tt2 - tt1
        t5 = time.time()
        tweets.sort(key=lambda x: x['ts'], reverse=True)
        t6 = time.time()

        timer['op_lock'] = t1 - t0
        timer['cache_get_tweet_ids'] = t2 - t1
        timer['cache_pop_tweets'] = t3 - t2
        timer['cache_get_tweet'] = t4 - t3
        timer['db_get_tweet'] = t_get_tweet
        timer['cache_set_tweet'] = t_set_cache
        timer['op_sort'] = t6 - t5

        return tweets


class FeedPushWriteBehind(FeedPushCacheAside):
    '''
    Getting tweets is the same as FeedPushCacheAside.
    Creating tweets writes to the same global cache FeedPushCacheAside uses,
    and also writes to a queue (list) so they can be persisted later.
    A worker runs in the background which flushes new data to db periodically.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key_newtweets = self.get_key('feedpush-newtweets')
        self.name_persistlock = 'persist-lock'
        self.interval = conf['write-behind-interval']
        self.batchsize = conf['write-behind-batchsize']
        self.add_background_task('push-writebehind-persistence_worker', self._persistence_worker)


    async def _persistence_worker(self):
        t0 = time.time()
        while 1:
            now = time.time()
            elapsed = now - t0
            await asyncio.sleep(self.interval - elapsed)
            lock_acquired = await self.lock(self.name_persistlock, blocking=False)
            if not lock_acquired:
                await asyncio.sleep(random.random() * 0.5 * self.interval)
            else:
                t0 = time.time()
                logger.debug('running')
                total = 0
                while 1:
                    # find all tweets whose score(ts) > last_latest
                    new_tweet_ids = await redis.lrange(self.key_newtweets, 0, self.batchsize - 1, encoding='utf8')
                    n = len(new_tweet_ids)
                    if n == 0:
                        break
                    # retrieve tweet content
                    new_tweet_keys = (self.get_key(self.prefix_cache, tid) for tid in new_tweet_ids)
                    new_tweets = await redis.mget(*new_tweet_keys, encoding='utf8')
                    # write them to db
                    new_tweets = map(json.loads, new_tweets)
                    asyncio.gather(
                        tweet.create_many(new_tweets),
                        redis.ltrim(self.key_newtweets, n, -1)
                    )
                    total += n
                    if n < self.batchsize:
                        break
                elapsed = time.time() - t0
                logger.debug('persisted {} tweets. time {}'.format(total, elapsed))
                # unlock after a period so other processes won't persist again
                # shortly after this process finishes
                await self.unlock(self.name_persistlock, after=0.9*(self.interval-elapsed))


    async def create(self, user_id, tweet_id, content, timestamp, **kwargs):
        '''
        only write to cache
        let background worker flush them to db
        '''
        logger.debug('user_id {} tweet_id {} ts {}'.format(
            user_id, tweet_id, timestamp))
        timer = kwargs.get('timer', {})
        # add tweet to global cache
        twt = json.dumps({
            'user_id': user_id,
            'tweet_id': tweet_id,
            'content': content,
            'ts': timestamp
        })
        t0 = time.time()
        t_add_global = redis.set(self.get_key(self.prefix_cache, tweet_id), twt)
        t_add_track = redis.rpush(self.key_newtweets, tweet_id)
        await asyncio.gather(t_add_global, t_add_track)
        t1 = time.time()
        # add tweet id to the feed list of all followers
        followers = await user_follow.all_followers(user_id)
        t2 = time.time()
        # add tweets to the queue waiting to be persisted
        await self.lock(self.name_feedlock)
        t3 = time.time()
        t_feedlist = (redis.lpush(self.get_key(flr), tweet_id)
                        for flr in followers)
        await asyncio.gather(*t_feedlist)
        t4 = time.time()
        await self.unlock(self.name_feedlock)
        timer['cache_set_tweet'] = t1 - t0
        timer['db_get_follower'] = t2 - t1
        timer['op_lock'] = t3 - t2
        timer['cache_push_feedlist'] = t4 - t3
        return 0
