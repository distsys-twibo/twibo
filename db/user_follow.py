import logging

from db.db_utils import db, exists

logger = logging.getLogger(__name__)

coll = db['follow']


def follow(user_id, followees):
    coll.insert_many(({
        'user_id': user_id,
        'target': f
    } for f in followees))


def is_following(user_id, target):
    return exists(coll, {
        'user_id': user_id,
        'target': target
    })


def is_followed_by(user_id, target):
    return exists(coll, {
        'user_id': target,
        'target': user_id
    })


def all_followees(user_id):
    return (f['target'] for f in coll.find({'user_id': user_id}))


def all_followers(user_id):
    return (f['user_id'] for f in coll.find({'target': user_id}))
