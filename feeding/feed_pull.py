import logging
import heapq
import time

from db import tweet, user_follow
from .base_feeder import BaseFeeder


logger = logging.getLogger(__name__)


class FeedPull(BaseFeeder):
    prefix = 'feedpull'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create(self, user_id, tweet_id, content, timestamp, **kwargs):
        logger.debug('user_id {} tweet_id {} ts {}'.format(
            user_id, tweet_id, timestamp))
        timer = kwargs.get('timer', {})
        t0 = time.time()
        ret = await tweet.create(user_id, tweet_id, content, timestamp)
        t1 = time.time()
        timer['db_create'] = t1 - t0
        return ret

    async def get(self, user_id, limit, **kwargs):
        logger.debug('user_id {} limit {}'.format(user_id, limit))
        timer = kwargs.get('timer', {})
        t0 = time.time()
        followees = await user_follow.all_followees(user_id)
        t1 = time.time()
        feeds = []
        # get @limit feeds from each of the followees
        # then get the newest @limit feeds among them
        for fle in followees:
            feeds += await tweet.get_by_user_id(fle, limit)
        t2 = time.time()
        feeds = heapq.nlargest(limit, feeds, key=lambda x: x['ts'])
        t3 = time.time()
        timer['db_get_followee'] = t1 - t0
        timer['db_get_feeds'] = t2 - t1
        timer['op_sort'] = t3 - t2
        return feeds


# There's no FeedPullCacheAside because caching tweets requires that we first
# know which tweet ids are required/wanted,
# which requires a per-user feed list,
# which doesn't exist...
