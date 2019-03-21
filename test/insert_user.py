import sys

import requests


url_create = 'http://localhost:9990/user/create'
url_follow = 'http://localhost:9990/user/follow'


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
    rels.append((a, b))

print('{} users, {} relations'.format(len(users), len(rels)))

for u in users:
    print('add', u)
    requests.post(url_create, data={
        'uid': u,
        'info': ''
    })

for a, b in rels:
    print('follow', a, b)
    requests.post(url_follow, data={
        'uid': a,
        'target_ids': b
    })
