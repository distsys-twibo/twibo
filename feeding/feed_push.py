import asyncio
import logging
import heapq

from caching.caching_utils import redis
from db import tweet, user_follow
from .base_feeder import BaseFeeder


logger = logging.getLogger(__name__)


class FeedPush(BaseFeeder):
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
