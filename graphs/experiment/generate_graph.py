# @Time    : 4/1/2019 3:35 PM
# @Author  : Weitian Xing
# @FileName: print_graph.py

import matplotlib.pyplot as plt
import numpy as np
from extract_info import extract
from matplotlib import ticker

prefix = "push_wb_"

ave_2 = extract("results_2m.csv", prefix)
ave_4 = extract("results_4m.csv", prefix)
ave_8 = extract("results_8m.csv", prefix)
ave_16 = extract("results_16m.csv", prefix)
ave_32 = extract("results_32m.csv", prefix)

tick_spacing = 50

# plt.figure(figsize=(10, 4))

plt.xlim((0, 300))
plt.ylim((0, 1))

plt.xlabel("Elapsed Time In Test (secs)")
plt.ylabel("Hit Rate (percentage)")

my_x_ticks = np.arange(0, 300, 5)
plt.xticks(my_x_ticks)
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

x = range(0, 300, 5)
l1, = plt.plot(x, ave_2[:-1], markersize=6, marker='.', label='2M')
l2, = plt.plot(x, ave_4[:-1], markersize=6, marker='.', label='4M')
l3, = plt.plot(x, ave_8[:-1], markersize=6, marker='.', label='8M')
l4, = plt.plot(x, ave_16[:-1], markersize=6, marker='.', label='16M')
l5, = plt.plot(x, ave_32[:-1], markersize=6, marker='.', label='32M')

plt.legend(handles=[l1, l2, l3, l4, l5], labels=['2M',
                                                 '4M',
                                                 '8M',
                                                 '16M',
                                                 '32M'], loc=4)

plt.grid()
plt.savefig('push_wb_results.png', bbox_inches='tight')
plt.show()
