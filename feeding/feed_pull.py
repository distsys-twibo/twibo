import logging
import heapq

from db.db_utils import db_r
from db import user_follow
from .base_feeder import BaseFeeder


logger = logging.getLogger(__name__)


class FeedPull(BaseFeeder):
    prefix = 'feedpull'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create(self, user_id, tweet_id, timestamp):
        '''adds a new tweet to the user's feed list'''
        logger.debug('user_id {} tweet_id {} ts {}'.format(
            user_id, tweet_id, timestamp))
        return db_r.zadd(self.get_key(user_id), {tweet_id: timestamp})

    async def get(self, user_id, limit):
        followees = user_follow.all_followees(user_id)
        feeds = []
        # get @limit feeds from each of the followees
        # then get the newest @limit feeds among them
        for fle in followees:
            feeds += db_r.zrevrange(self.get_key(fle),
                                    0, limit, withscores=True)
        feeds = heapq.nlargest(limit, feeds, key=lambda x: x[1])
        return feeds


fp = FeedPull()
