import logging

from db.db_utils import db

logger = logging.getLogger(__name__)


coll = db['user']
coll.create_index('user_id')


def create(user_id, extra_info):
    coll.insert_one({
        'user_id': user_id,
        'info': extra_info
    })

def get(user_id):
    return coll.find_one({
        'user_id': user_id
    })
