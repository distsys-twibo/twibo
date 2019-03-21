import logging
import time

from aiohttp import web

from db import user
from db import user_follow


logger = logging.getLogger(__name__)

routes = web.RouteTableDef()


@routes.post('/user/create')
async def create(request):
    data = await request.post()
    user_id = data['user_id']
    info = data.get('info', '')
    await user.create(user_id, info)
    return web.Response(text='0')


@routes.post('/user/create_many')
async def create_many(request):
    data = await request.json()
    users = data['users']
    await user.create_many(users)
    return web.Response(text='0')


@routes.get('/user/get')
async def get(request):
    query = request.rel_url.query
    user_id = query['user_id']

    t1 = time.time()
    u = await user.get(user_id)
    fle = await user_follow.all_followees(user_id)
    flr = await user_follow.all_followers(user_id)
    t2 = time.time()
    return web.json_response({
        'user': u,
        'followees': fle,
        'followers': flr,
        'times': {
            'full': t2 - t1
        }
    })


@routes.post('/user/follow')
async def follow(request):
    data = await request.post()
    user_id = data['user_id']
    target_ids = data['target_ids'].split(',')
    ids = (await user_follow.follow(user_id, target_ids)).inserted_ids
    return web.Response(text=str(len(ids)))


@routes.post('/user/follow_many')
async def follow_many(request):
    data = await request.post()
    relations = data['relations']
    relations = relations.split(',')
    relations2 = []
    for rel in relations:
        a, b = rel.split(' ')
        relations2.append((a, b))
    logger.debug('inserting {} relations'.format(len(relations2)))
    await user_follow.follow_many(relations2)
    return web.Response(text='0')
