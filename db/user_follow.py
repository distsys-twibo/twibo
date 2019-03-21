import asyncio
import logging

from db.db_utils import db, exists

logger = logging.getLogger(__name__)

coll = db['follow']
asyncio.gather(
    coll.create_index('user_id'),
    coll.create_index('target')
)


async def follow(user_id, followees):
    return await coll.insert_many(({
        'user_id': user_id,
        'target': f
    } for f in followees))


async def is_following(user_id, target):
    return await exists(coll, {
        'user_id': user_id,
        'target': target
    })


async def is_followed_by(user_id, target):
    return await exists(coll, {
        'user_id': target,
        'target': user_id
    })


async def all_followees(user_id):
    cursor = coll.find({'user_id': user_id})
    ret = [f['target'] async for f in cursor]
    return ret


async def all_followers(user_id):
    cursor = coll.find({'target': user_id})
    ret = [f['user_id'] async for f in cursor]
    return ret
