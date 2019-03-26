from collections import defaultdict
import random
import string
import sys


def parse_lines(lines):
    ret = []
    for l in lines:
        ts, action, user_id, tlen = l.split('\t')
        ret.append([float(ts), action, user_id, int(tlen)])
    return ret


def normalize_length(activities, min_len, max_len):
    for a in activities:
        if a[1] == 'Publish':
            l = a[3]
            while l > max_len:
                l //= 5
            a[3] = l


chars = string.ascii_letters + string.digits
def random_string(length):
    return ''.join(random.choice(chars) for _ in range(length))


def save_timer(calcers, timer):
    for k, v in timer.items():
        calcers[k].add(v)


def print_calcers(calcers):
    calcers = sorted(calcers.items(), key=lambda x: x[0])
    for n, c in calcers:
        avg = c.avg()
        print('{}:{}:{:.2f}:{:.8f}'.format(n, c.count, 1 / (avg+1e-10), avg))


class Calcer:
    def __init__(self, *args, **kwargs):
        self.val = 0.0
        self.count = 0

    def add(self, v):
        if v is not None:
            self.val += v
            self.count += 1

    def avg(self):
        if self.count != 0:
            return self.val / self.count
        return -1
