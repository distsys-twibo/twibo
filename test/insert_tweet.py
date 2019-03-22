import sys

import requests


url_create = 'http://localhost:9990/tweet/create'


if len(sys.argv) != 2:
    print('args: file_name')
    exit(1)

fn = sys.argv[1]

with open(fn) as f:
    lines = [_ for _ in f.read().splitlines() if not _.startswith('#')]

tweets = []

for l in lines:
    sp = l.split('#~#')
    tweet_id, u, t, c = sp[0], sp[1], sp[2], sp[3]
    tweets.append((tweet_id, u, t, c))

print('{} tweets'.format(len(tweets)))

for tweet_id, u, t, c in tweets:
    print('post', tweet_id, u, t, c)
    requests.post(url_create, data={
        'tweet_id': tweet_id,
        'user_id': u,
        'ts': t,
        'content': c
    })
