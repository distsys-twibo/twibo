from . import feed_pull

feeders = {
    'pull': feed_pull.FeedPull(),
    'pull-cacheaside': feed_pull.FeedPullCacheAside()
}
