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
activity_file = ''
# max length of a tweet
t_maxlen = 400


class Transaction(object):
    def __init__(self):
        self.f = open(activity_file)
        self.tid_prefix = socket.gethostname()
        self.s = requests.session()

    def next_act(self):
        l = self.f.readline()
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
            respj = resp.json()
            for k, v in respj['timer'].iteritems():
                self.custom_timers['get_{}'.format(k)] = v
        else:
            resp = self.s.post(url_create, data={
                'tweet_id': self.tid_prefix + '-' + str(ts) + '-' + utils.random_string(6),
                'user_id': user_id,
                'ts': ts,
                'content': utils.random_string(tlen)
            })
            respj = resp.json()
            for k, v in respj['timer'].iteritems():
                self.custom_timers['create_{}'.format(k)] = v


if __name__ == '__main__':
    trans = Transaction()
    trans.run()
