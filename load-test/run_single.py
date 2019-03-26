from pprint import pprint
import sys
import socket
import time

import requests

import utils

url_base = 'http://localhost:9991'
url_create = url_base + '/tweet/create'
url_get = url_base + '/tweet/get'


def main():
    if len(sys.argv) != 2:
        print('args: file_name')
        exit(1)

    print('loading data')
    fn = sys.argv[1]
    with open(fn) as f:
        lines = f.read().splitlines()
    activities = utils.parse_lines(lines)
    num = len(activities)
    print('data loaded. {} activities'.format(num))
    print('normalize content length')
    utils.normalize_length(activities, 1, 400)

    tid_prefix = socket.gethostname()
    print('begin. prefix of tweet_id is {}'.format(tid_prefix))
    t0 = time.time()
    c = 0
    cal_create = utils.Calcer()
    cal_db_get_feeds = utils.Calcer()
    cal_db_get_rel_followee = utils.Calcer()
    for ts, action, user_id, tlen in activities:
        if action == 'Retrieve':
            resp = requests.get(url_get, params={
                'user_id': user_id,
                'limit': 50,
                'pop': 0
            })
        else:
            resp = requests.post(url_create, data={
                'tweet_id': ts,
                'user_id': user_id,
                'ts': ts,
                'content': utils.random_string(tlen)
            })
        respj = resp.json()
        # pprint(respj)
        cal_create.add(respj['timer'].get('create', None))
        cal_db_get_feeds.add(respj['timer'].get('db_get_feeds', None))
        cal_db_get_rel_followee.add(respj['timer'].get('db_get_rel_followee', None))
        c += 1
        if c % 100 == 0:
            print(time.time() - t0, c, c / (time.time() - t0))
    t999 = time.time()
    duration = t999 - t0
    print('finished. {:.2f}, {:.2f}/s, {:.5f}/req'.format(duration, num / duration, duration / num))
    print('create {:.8f} db_get_feeds {:.8f}, db_get_rel_followee {:.8f}'.format(cal_create.avg(), cal_db_get_feeds.avg(), cal_db_get_rel_followee.avg()))

if __name__ == "__main__":
    main()
