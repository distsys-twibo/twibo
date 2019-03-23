import asyncio

from background import background_tasks
from caching.caching_utils import redis


class BaseFeeder:
    _prefix = 'twibo'
    prefix = 'base'

    def get_key(self, *args):
        return ':'.join([self._prefix, self.prefix, *args])

    def add_background_task(self, name, coro):
        background_tasks.append((name, coro))

    async def lock(self, lockname, blocking=True):
        # returns true if locked
        # if blocking, always return True
        k = self.get_key(lockname)
        acq = await redis.set(k, '1', exist=redis.SET_IF_NOT_EXIST)
        if not blocking:
            return acq
        while not acq:
            await asyncio.sleep(0.01)
            acq = await redis.set(k, '1', exist=redis.SET_IF_NOT_EXIST)
        return True


    async def unlock(self, lockname, after=0):
        # unlock a lock. if after > 0, then unlock after @after seconds
        if after == 0:
            return await redis.delete(self.get_key(lockname))
        else:
            return await redis.set(self.get_key(lockname), '2', expire=max(0, round(after)))

    async def create(self, user_id, tweet_id, content, timestamp, **kwargs):
        raise NotImplementedError

    async def get(self, user_id, limit, **kwargs):
        '''get newest @limit feeds from the followees of @user_id'''
        raise NotImplementedError
