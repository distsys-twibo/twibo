import logging
import heapq

from caching.caching_utils import redis
from db import tweet, user_follow
from .base_feeder import BaseFeeder


logger = logging.getLogger(__name__)


class FeedPull(BaseFeeder):
    prefix = 'feedpull'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create(self, user_id, tweet_id, content, timestamp):
        logger.debug('user_id {} tweet_id {} ts {}'.format(
            user_id, tweet_id, timestamp))
        return await tweet.create(user_id, tweet_id, content, timestamp)

    async def get(self, user_id, limit):
        logger.debug('user_id {} limit {}'.format(user_id, limit))
        followees = await user_follow.all_followees(user_id)
        feeds = []
        # get @limit feeds from each of the followees
        # then get the newest @limit feeds among them
        for fle in followees:
            feeds += await tweet.get(fle, limit)
        feeds = heapq.nlargest(limit, feeds, key=lambda x: x['ts'])
        return feeds
