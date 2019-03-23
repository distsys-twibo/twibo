class BaseFeeder:
    _prefix = 'twibo'
    prefix = 'base'

    def get_key(self, *args):
        return ':'.join([self._prefix, self.prefix, *args])

    async def create(self, user_id, tweet_id, content, timestamp, **kwargs):
        raise NotImplementedError

    async def get(self, user_id, limit, **kwargs):
        '''get newest @limit feeds from the followees of @user_id'''
        raise NotImplementedError
