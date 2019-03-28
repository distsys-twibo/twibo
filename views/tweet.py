import json
import logging
import time

from aiohttp import web

from feeding import feeders
from utils.config import conf


logger = logging.getLogger(__name__)

routes = web.RouteTableDef()

feeder = feeders[conf['feeder']]()
logger.warn('feeder is {}'.format(feeder))


@routes.post('/tweet/create')
async def create(request):
    data = await request.post()
    user_id = data['user_id']
    tweet_id = data['tweet_id']
    content = data['content']
    timestamp = float(data['ts'])
    timer = {}
    t1 = time.time()
    await feeder.create(user_id, tweet_id, content, timestamp, timer=timer)
    t2 = time.time()
    timer['full'] = t2 - t1
    return web.json_response({
        'timer': timer
    })


@routes.get('/tweet/get')
async def get(request):
    query = request.rel_url.query
    user_id = query['user_id']
    limit = int(query.get('limit', 10))
    pop = bool(int(query.get('pop', 0)))
    timer = {}
    t1 = time.time()
    tweets = await feeder.get(user_id, limit, pop=pop, timer=timer)
    t2 = time.time()
    timer['full'] = t2 - t1
    return web.json_response({
        'tweets': tweets,
        'timer': timer
    })
