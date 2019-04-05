# @Time    : 3/20/2019 7:49 PM
# @Author  : Weitian Xing
# @FileName: tmp.py

# followers
import matplotlib.pyplot as plt

a = dict()

with open("twitter_combined.txt", "r") as f:
    for each in f:
        b, c = each.split(" ")
        if "\n" in c:
            c = c.rstrip("\n")
        if c not in a:
            a[c] = 1
        else:
            a[c] = a[c] + 1
        if b not in a:
            a[b] = 0
p0 = 0
p1_10 = 0
p10_20 = 0
p20_50 = 0
p50_100 = 0
p100 = 0

for v in a.values():
    if v == 0:
        p0 += 1
    elif 0 < v < 10:
        p1_10 += 1
    elif 10 <= v < 20:
        p10_20 += 1
    elif 20 <= v < 50:
        p20_50 += 1
    elif 50 <= v < 100:
        p50_100 += 1
    else:
        p100 += 1

g = [p0, p1_10, p10_20, p20_50, p50_100, p100]
_sum = 0
for each in g:
    _sum = _sum + each

print(g)
print(_sum)

plt.bar(range(6), g, width=0.35, align='center', color='steelblue', alpha=0.8)
plt.ylabel('number of accounts')
plt.xlabel('followers')
plt.xticks(range(6), ['0', '1~10', '10~20', '20~50', '50-100', '>=100'])
for a, b in zip(range(6), g):
    plt.text(a, b, '%.0f' % b, ha='center', va='bottom', fontsize=7)
plt.savefig('followers.png', bbox_inches='tight')
plt.show()

# ----

# followees
# import matplotlib.pyplot as plt
#
# a = {}
# _sum = 0
# with open("twitter_combined.txt", "r") as f:
#     for each in f:
#         b, c = each.split(" ")
#         if "\n" in c:
#             c = c.rstrip("\n")
#         if b not in a:
#             a[b] = 1
#         else:
#             a[b] = a[b] + 1
#         if c not in a:
#             a[c] = 0
# p0 = 0
# p1_10 = 0
# p10_20 = 0
# p20_50 = 0
# p50_100 = 0
# p100 = 0
#
# for v in a.values():
#     if v == 0:
#         p0 += 1
#     elif 0 < v < 10:
#         p1_10 += 1
#     elif 10 <= v < 20:
#         p10_20 += 1
#     elif 20 <= v < 50:
#         p20_50 += 1
#     elif 50 <= v < 100:
#         p50_100 += 1
#     else:
#         p100 += 1
#
# g = [p0, p1_10, p10_20, p20_50, p50_100, p100]
#
# for each in g:
#     _sum += each
# print(g)
# print(_sum)
#
# plt.bar(range(6), g, width=0.35, align='center', color='steelblue', alpha=0.8)
# plt.ylabel('number of accounts')
# plt.xlabel('followees')
# plt.xticks(range(6), ['0', '1~10', '10~20', '20~50', '50-100', '>=100'])
# for a, b in zip(range(6), g):
#     plt.text(a, b, '%.0f' % b, ha='center', va= 'bottom',fontsize=7)
# plt.savefig('followees.png', bbox_inches='tight')
# plt.show()


# average followees
# a = {}
# with open("twitter_combined.txt", "r") as f:
#     for each in f:
#         b, c = each.split(" ")
#         if "\n" in c:
#             c.rstrip("\n")
#         if b not in a:
#             a[b] = 1
#         else:
#             a[b] += 1
#         if c not in a:
#             a[c] = 0
# _sum = 0
# for v in a.values():
#     _sum += v
#
# print(_sum)
# print(len(a))
# print(_sum / len(a)) # 15.98
#
# _z = []
# for each in a.values():
#     _z.append(each)
# _z = sorted(_z)
# print(_z)
# import numpy as np
# print(np.median(_z))

# print(max(a.values()))
# print(min(a.values()))


# average followers
# a = {}
# with open("twitter_combined.txt", "r") as f:
#     for each in f:
#         b, c = each.split(" ")
#         if "\n" in c:
#             c = c.rstrip("\n")
#         if c not in a:
#             a[c] = 1
#         else:
#             a[c] += 1
#         if b not in a:
#             a[b] = 0
#
# _sum = 0
# for v in a.values():
#     _sum += v
# print(_sum / len(a))
#
# _z = []
# for each in a.values():
#     _z.append(each)
# _z = sorted(_z)
# print(_z)
# import numpy as np
# print(np.median(_z))
#
# print(max(a.values()))
# print(min(a.values()))
