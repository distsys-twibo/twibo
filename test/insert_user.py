import sys
import json

import requests


url_create = 'http://localhost:9991/user/create_many'
url_follow = 'http://localhost:9991/user/follow_many'


if len(sys.argv) != 2:
    print('args: file_name')
    exit(1)

fn = sys.argv[1]


with open(fn) as f:
    lines = [_ for _ in f.read().splitlines() if not _.startswith('#')]

users = set()
rels = []

for l in lines:
    sp = l.split(' ')
    a, b = sp[0], sp[1]
    users.add(a)
    users.add(b)
    rels.append(l)

nuser = len(users)
nrel = len(rels)
print('{} users, {} relations'.format(nuser, nrel))


def create_many(b):
    data = {
        'users': [{
            'user_id': uid,
            'info': ''
        } for uid in b]
    }
    requests.post(url_create, json=data)


nbatch = 1000
batch = []


for i, u in enumerate(users):
    if i % nbatch == 0:
        print('add {}/{}'.format(i, nuser))
    batch.append(u)
    if len(batch) == nbatch:
        create_many(batch)
        batch = []
if len(batch) != 0:
    create_many(batch)
    batch = []


def follow_many(b):
    requests.post(url_follow, data={
        'relations': ','.join(b)
    })


for i, r in enumerate(rels):
    if i % nbatch == 0:
        print('follow {}/{}'.format(i, nrel))
    batch.append(r)
    if len(batch) == nbatch:
        follow_many(batch)
        batch = []
if len(batch) != 0:
    follow_many(batch)
    batch = []
