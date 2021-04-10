import sys
import itertools
import numpy as np
from datetime import datetime
import operator
from collections import defaultdict

no_baskets = 0
no_pretinac = 0
s = 0
baskets = []
br_predmeta = defaultdict(int)
# pretinci = {}
parovi = defaultdict(int)
threshold = 0
pretinci = []


class Helper:
    def __init__(self, k_value, condition):
        self.cond = condition
        self.k_value = k_value


def hash_tuple(i, j, l):
    return ((i * l) + j) % no_pretinac


i = 0
combinations = defaultdict(int)
helpers = {}
for line in sys.stdin:
    if i == 0:
        no_baskets = int(line.rstrip())
    elif i == 1:
        threshold = float(line.rstrip()) * no_baskets
    elif i == 2:
        no_pretinac = int(line.rstrip())
        pretinci = np.zeros(no_pretinac)
    elif i <= no_baskets + 2:
        int_array = [int(a) for a in line.rstrip().split(" ")]
        for i, j in itertools.combinations(int_array, 2):
            combinations[(i, j)] += 1
        for item in int_array:
            br_predmeta[item] += 1
    i += 1
l = len(br_predmeta)

for (i, j) in combinations.keys():
    expression = br_predmeta[i] >= threshold and br_predmeta[j] >= threshold
    if expression == True:
        helpers[(i, j)] = Helper(hash_tuple(i, j, l), expression)

for (i, j), helper in helpers.items():
    pretinci[helper.k_value] += combinations[(i, j)]

for (i, j), helper in helpers.items():
    if pretinci[helper.k_value] >= threshold:
        parovi[(i, j)] += combinations[(i, j)]

print(len(helpers))
print(len(parovi))
parovi_temp = list(filter(lambda elem: elem >= threshold,parovi.values()))
sorted_d = sorted(parovi_temp, reverse=True)
print(*sorted_d, sep="\n", end="")
