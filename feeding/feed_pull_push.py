import asyncio
import logging
import heapq
import json
import time

from caching.caching_utils import redis
from db import tweet, user_follow
from .base_feeder import BaseFeeder
from utils.config import conf


logger = logging.getLogger(__name__)


class FeedPullPush(BaseFeeder):
    '''
    Keeps track of online users.
    Every online user has a feed list. If goes offline, delete the list.
    When creating a tweet, push to online followers' feed lists.
    When getting, if online, get from feed list;
    if was offline, mark online now and build feed list.
    '''
    prefix = 'feedpullpush'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create(self, user_id, tweet_id, content, timestamp, **kwargs):
        logger.debug('user_id {} tweet_id {} ts {}'.format(
            user_id, tweet_id, timestamp))
        pass
        return 0

    async def get(self, user_id, limit, **kwargs):
        pass
