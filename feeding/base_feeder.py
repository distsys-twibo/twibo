from db.db_utils import db_r


class BaseFeeder:
    _prefix = 'twibo'
    prefix = 'base'

    def get_key(self, *args):
        return ':'.join([self._prefix, self.prefix, *args])

    async def create(self, user_id, tweet_id, timestamp):
        raise NotImplementedError

    async def get(self, user_id, limit):
        '''get newest @limit feeds from the followees of @user_id'''
        raise NotImplementedError
