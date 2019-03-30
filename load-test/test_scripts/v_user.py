import random
import os
import socket
import sys
import time

import requests

sys.path.insert(0, os.getcwd())
import utils


url_base = 'http://127.0.0.1:9991'
url_create = url_base + '/tweet/create'
url_get = url_base + '/tweet/get'
# path to the output of SONETOR
activity_file = '/u7/j892zhang/mem/twibo/8w-sorted.txt'
# max length of a tweet
t_maxlen = 400

f = []
n_processes = 100
if n_processes == 1:
    f.append(open(activity_file))
else:
    # exhaustively open 100 input files...
    try:
        for i in range(n_processes):
            f.append(open(activity_file + '.{}'.format(i)))
    except:
        pass
print 'found {} input files'.format(len(f))


class Transaction(object):
    def __init__(self, n_processes=None):
        self.tid_prefix = socket.gethostname()
        self.s = requests.session()
        # will be overriden by multimechnize
        self.process_num = 0

    def next_act(self):
        l = f[self.process_num].readline()
        act = utils.parse_line(l)
        utils.norm_act(act, 1, t_maxlen)
        return act

    def run(self):
        self.custom_timers = {}
        ts, action, user_id, tlen = self.next_act()
        if action == 'Retrieve':
            resp = self.s.get(url_get, params={
                'user_id': user_id,
                'limit': 50,
                'pop': 0
            })
            pref = 'get'
        else:
            resp = self.s.post(url_create, data={
                'tweet_id': self.tid_prefix + '-' + str(ts) + '-' + utils.random_string(6),
                'user_id': user_id,
                'ts': ts,
                'content': utils.random_string(tlen)
            })
            pref = 'create'

        try:
            respj = resp.json()
            for k, v in respj['timer'].iteritems():
                self.custom_timers['{}_{}'.format(pref, k)] = v
        except Exception as e:
            print 'exception: {}. {} {} {} {}\nresp:{}: {}'.format(e, ts, action, user_id, tlen, resp.status_code, resp.text)
            raise e


if __name__ == '__main__':
    trans = Transaction(8)
    while 1:
        trans.run()
