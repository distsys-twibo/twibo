from background import background_tasks
from caching.caching_utils import redis


class BaseFeeder:
    _prefix = 'twibo'
    prefix = 'base'

    def get_key(self, *args):
        return ':'.join([self._prefix, self.prefix, *args])

    def add_background_task(self, name, coro):
        background_tasks.append((name, coro))

    async def lock(self, lockname):
        # non-blocking; returns true if locked
        return await redis.set(self.get_key(lockname), '1', exist=redis.SET_IF_NOT_EXIST)

    async def unlock(self, lockname):
        return await redis.delete(self.get_key(lockname))

    async def create(self, user_id, tweet_id, content, timestamp, **kwargs):
        raise NotImplementedError

    async def get(self, user_id, limit, **kwargs):
        '''get newest @limit feeds from the followees of @user_id'''
        raise NotImplementedError
