import requests


url_create = 'http://localhost:9990/tweet/create'


with open('tweets.txt') as f:
    lines = [_ for _ in f.read().splitlines() if not _.startswith('#')]

tweets = []

for l in lines:
    sp = l.split('#~#')
    tid, u, t, c = sp[0], sp[1], sp[2], sp[3]
    tweets.append((tid, u, t, c))

print('{} tweets'.format(len(tweets)))

for tid, u, t, c in tweets:
    print('post', tid, u, t, c)
    requests.post(url_create, data={
        'tid': tid,
        'uid': u,
        'ts': t,
        'content': c
    })
