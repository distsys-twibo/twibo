# @Time    : 4/1/2019 3:32 PM
# @Author  : Weitian Xing
# @FileName: extract_info.py


import csv
import json
import statistics
from math import floor


def extract(path, prefix):
    tmp = []

    with open(prefix + path, newline='') as csvfile:
        _reader = csv.reader(csvfile)
        for row in _reader:
            row_str_dict = ",".join(row[6:])
            row_str_dict = row_str_dict.replace('\'', '"')
            row_json = json.loads(row_str_dict)
            if "create_full" not in row_json:
                if row_json['get_op_cache_try'] != 0:
                    row_json['time'] = row[1]
                    tmp.append(row_json)

    data = {}

    ave = []

    for i in range(0, 61):
        data[i] = []

    for each in tmp:
        number = floor(float(each['time']) / 5)
        data[number].append(each)

    for each in data.values():
        m = []
        for e in each:
            m.append(e['get_op_cache_rate'])
        _average = statistics.mean(m)
        ave.append(_average)

    # total average
    total_average = []
    for each in data.values():
        for e in each:
            total_average.append(e['get_op_cache_rate'])
    print(statistics.mean(total_average))

    return ave
