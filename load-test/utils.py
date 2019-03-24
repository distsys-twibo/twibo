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
    return ''.join(random.choices(chars, k=length))
