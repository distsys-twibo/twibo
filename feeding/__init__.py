from . import feed_pull
from . import feed_push

feeders = {
    'pull': feed_pull.FeedPull,
    'push': feed_push.FeedPush,
    'push-cacheaside': feed_push.FeedPushCacheAside,
    'push-writebehind': feed_push.FeedPushWriteBehind
}
