import os
import sys
from itertools import combinations
import math
import copy

user = ""
n = 0
k = 0
ratings = []
items = []
users = []
item_info = {}
user_info = {}
weights = {}
temp = []

user = sys.argv[2]
n = int(sys.argv[3])
k = int(sys.argv[4])

with open(sys.argv[1]) as ratings_dataset:
    for line in ratings_dataset:
        ratings.append(line.strip('\n').replace('\t', '*').split('*'))

for r in ratings:
    r[1] = float(r[1])
    if r[2] not in items:
        items.append(r[2])
    if r[0] not in users:
        users.append(r[0])

item_info = {item:[] for item in items}
user_info = {user:[] for user in users}
for r in ratings:
    item_info[r[2]].append([r[0], r[1]])
    user_info[r[0]].append([r[2], r[1]])

for pair in ["*".join(map(str,comb)) for comb in combinations(items, 2)]:
    weights[tuple(pair.split('*'))] = 10.0

def similarity(weights = {}, item_info = {}):
    for pair in weights:
        item_i = []
        item_j = []
        sumi = 0.0
        sumj = 0.0
        num = 0.0
        dnom_comp1 = 0.0
        dnom_comp2 = 0.0
        avgri = 0.0
        avgrj = 0.0
        for li in item_info[list(pair)[0]]:
            for lj in item_info[list(pair)[1]]:
                if li[0] == lj[0]:
                    item_i.append(li)
                    item_j.append(lj)
        item_i.sort()
        item_j.sort()
        if (len(item_i) == 0 and len(item_j) == 0):
            weights[pair] = 0.0
        else:
            for i in item_i:
                sumi += i[1]
            avgri = float(sumi/len(item_i))
            for j in item_j:
                sumj += j[1]
            avgrj = float(sumj/len(item_j))
            for s in range(len(item_i)):
                num += (item_i[s][1] - avgri) * (item_j[s][1] - avgrj)
                dnom_comp1 += (item_i[s][1] - avgri) ** 2
                dnom_comp2 += (item_j[s][1] - avgrj) ** 2
            dnom_comp1 = float(math.sqrt(dnom_comp1))
            dnom_comp2 = float(math.sqrt(dnom_comp2))
            if dnom_comp1 == 0.0 or dnom_comp2 == 0.0:
                weights[pair] = 0.0
            else:
                denom = float(dnom_comp1 * dnom_comp2)
                weights[pair] = float(num/denom)


similarity(weights, item_info)

def prediction(n, k, user, items = [], user_info = {}, item_info = {}, weights = {}):
    user_ratings = {}
    for ir in user_info[user]:
        user_ratings[ir[0]] = ir[1]
    items_rated = []
    items_unrated = []
    predictions = []
    for item in user_ratings:
        items_rated.append(item)
    for item in items:
        if item not in items_rated:
            items_unrated.append(item)

    for iur in items_unrated:
        similar_rated_items = []
        for item in user_ratings:
            extra1 = [iur, item]
            extra2 = [item, iur]
            if tuple(extra1) in weights:
                similar_rated_items.append([item, user_ratings[item], weights[tuple(extra1)]])
            else:
                similar_rated_items.append([item, user_ratings[item], weights[tuple(extra2)]])
        similar_rated_items.sort(key = lambda x: x[0])
        similar_rated_items.sort(key = lambda x: x[2], reverse=True)
        similar_rated_items = similar_rated_items[0:n]
        num = 0.0
        denom = 0.0
        for sri in similar_rated_items:
            num += sri[1] * sri[2]
            denom += abs(sri[2])

        if denom == 0.0:
            predicted_rating = 0.0
        else:
            predicted_rating = float(num/denom)
        predictions.append([iur, predicted_rating])

    predictions = sorted(predictions)
    predictions.sort(key = lambda x: x[1], reverse=True)
    if k > len(predictions):
        for item in range(len(predictions)):
            print predictions[item][0], round(predictions[item][1], 5)
    else:
        for item in range(k):
            print predictions[item][0], round(predictions[item][1], 5)

prediction(n, k, user, items, user_info, item_info, weights)


