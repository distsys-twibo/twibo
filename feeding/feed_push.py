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

    async def create(self, user_id, tweet_id, content, timestamp):
        logger.debug('user_id {} tweet_id {} ts {}'.format(
            user_id, tweet_id, timestamp))
        followers = await user_follow.all_followers(user_id)
        t_db = tweet.create(user_id, tweet_id, content, timestamp)
        # add tweet id to the feed list of all followers
        t_feedlist = (redis.zadd(self.get_key(flr), timestamp, tweet_id)
                        for flr in followers)
        await asyncio.gather(t_db, *t_feedlist)
        return 0

    async def get(self, user_id, limit, pop=False):
        logger.debug('user_id {} limit {}'.format(user_id, limit))
        # get the ids of latest @limit tweets from the user's feed list
        tweet_ids = await redis.zrevrange(self.get_key(user_id), 0, limit)
        # get the actual tweet
        tweets = await tweet.get_by_tweet_ids(tweet_ids)
        return tweets
