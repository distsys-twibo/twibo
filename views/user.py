import logging

from aiohttp import web

from db import user
from db import user_follow


logger = logging.getLogger(__name__)

routes = web.RouteTableDef()


@routes.post('/user/create')
async def create(request):
    data = await request.post()
    user_id = data['uid']
    info = data['info']
    await user.create(user_id, info)
    return web.Response(text='0')


@routes.get('/user/get')
async def get(request):
    query = request.rel_url.query
    user_id = query['uid']
    u = await user.get(user_id)

    fle = await user_follow.all_followees(user_id)
    flr = await user_follow.all_followers(user_id)
    return web.Response(text=str({
        'user': u,
        'followees': fle,
        'followers': flr
    }))


@routes.post('/user/follow')
async def follow(request):
    data = await request.post()
    user_id = data['uid']
    target_ids = data['target_ids'].split(',')
    ids = (await user_follow.follow(user_id, target_ids)).inserted_ids
    return web.Response(text=str(len(ids)))
