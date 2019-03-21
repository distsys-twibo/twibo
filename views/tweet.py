import json
import logging

from aiohttp import web

from db import tweet


logger = logging.getLogger(__name__)

routes = web.RouteTableDef()


@routes.post('/tweet/create')
async def create(request):
    data = await request.post()
    user_id = data['uid']
    tweet_id = data['tid']
    content = data['content']
    timestamp = data['ts']
    await tweet.create(user_id, tweet_id, content, timestamp)
    return web.Response(text='0')


@routes.get('/tweet/get')
async def get(request):
    query = request.rel_url.query
    user_id = query['uid']
    limit = int(query.get('limit', 10))
    tweets = await tweet.get(user_id, limit)
    return web.json_response({'tweets': tweets})
