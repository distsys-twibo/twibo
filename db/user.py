import asyncio
import logging

from db.db_utils import db

logger = logging.getLogger(__name__)


coll = db['user']
asyncio.gather(
    coll.create_index('user_id')
)


async def create_many(users):
    return await coll.insert_many(users)


async def create(user_id, info):
    return await create_many([{
        'user_id': user_id,
        'info': info
    }])


async def get(user_id):
    return await coll.find_one({
        'user_id': user_id
    }, {'_id': False})
