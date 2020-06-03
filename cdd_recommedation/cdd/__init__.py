#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/5/21 15:12
# @Author : Kai
# @File : __init__.py.py
# @Software: PyCharm

import cdd_mysql
import math

user_id = 1
user_list = {}
# 数据预处理
def load_data():
    dataList = cdd_mysql.loadData()
    for rec in dataList:
        user = rec['user_id']
        article = rec['article_id']
        rating = rec['browse_value']
        # print("%s %s %s" % (user, article, rating))
        user_list.setdefault(user, {})
        user_list[user][article] = float(rating)

# 计算欧几里得距离
# user_diff[user_i][article_j] = diff => difference between user_i & user_id on article_j
def calculate():
    user_diff = {}
    for article in user_list[user_id]:
        for user_i in user_list.keys():
            user_diff.setdefault(user_i, {})
            for article_j in user_list[user_i].keys():
                if article == article_j:
                    diff = math.sqrt(pow(user_list[user_id][article] - user_list[user_i][article_j], 2))
                    user_diff[user_i][article_j] = diff
    return user_diff

# 求距离平均值 -> 求相似度 = 1 / (1 + 距离平均值) 加1防止除0
# 相似度与距离成反比
def people_rating():
    user_diff = calculate()
    rating = {}
    for people in user_diff.keys():
        rating.setdefault(people, {})
        a = 0
        b = 0
        # print("user ： %s" % people)
        for score in user_diff[people].values():
            a += score
            b += 1
        if(a == 0 and b == 0):
            rating[people] = 0
            continue
        # print(a, b)
        rating[people] = float(1 / (1 + (a/b)))
    return rating

def recommend():
    list = people_rating() # list为用户相似度的dictionary
    items = list.items()
    print(items)
    rank = [[v[1], v[0]] for v in items]  # rank为用户相似度的list
    print(rank)
    rank.sort(reverse = True)
    print(rank[0:10])

    recommend_list = get_recommend(rank[0 : 10])
    return recommend_list

def get_recommend(similarUserList):
    print("get_recommend: %s" % similarUserList)
    article_list = []
    for useri in similarUserList:
        for article, val in user_list[useri[1]].items():
            if article not in user_list[user_id].keys() and val >= 5:
                article_list.append(article)
                print("user: %s, article: %s, val = %s" % (useri, article, val))
    if(len(article_list) >= 20):
        return article_list[0: 20]
    else:
        return article_list[0: len(article_list)]


if __name__ == "__main__":
    load_data()
    cdd_mysql.clearTable()
    recomment_list = []

    for uid in user_list.keys():
        user_id = uid
        recomment_list = recommend()
        for article_i in recomment_list:
            cdd_mysql.outputData(user_id, article_i)