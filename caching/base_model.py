class BaseModel:
    _prefix = 'twibo'
    prefix = 'base'

    def __init__(self, *args, **kwargs):
        pass

    def get_key(self, *args):
        return ':'.join((self._prefix, self.prefix, *args))
