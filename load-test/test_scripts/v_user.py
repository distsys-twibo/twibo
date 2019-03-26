import random
import os
import socket
import sys
import time

import requests

sys.path.insert(0, os.getcwd())
import utils


url_base = 'http://somewhere:9991'
url_create = url_base + '/tweet/create'
url_get = url_base + '/tweet/get'
# path to the output of SONETOR
activity_file = ''
# max length of a tweet
t_maxlen = 400

class Transaction(object):
    def __init__(self):
        with open(activity_file) as f:
            lines = f.read().splitlines()
        self.activities = utils.parse_lines(lines)
        self.len = len(self.activities)
        utils.normalize_length(self.activities, 1, t_maxlen)
        self.tid_prefix = socket.gethostname()
        self.i = 0

    def next_act(self):
        act = self.activities[self.i]
        self.i = (self.i + 1) % self.len
        return act

    def run(self):
        ts, action, user_id, tlen = self.next_act()
        if action == 'Retrieve':
            resp = requests.get(url_get, params={
                'user_id': user_id,
                'limit': 50,
                'pop': 0
            })
            respj = resp.json()
            for k, v in respj['timer'].iteritems():
                self.custom_timers['get_{}'.format(k)] = v
        else:
            resp = requests.post(url_create, data={
                'tweet_id': self.tid_prefix + '-' + str(ts),
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
