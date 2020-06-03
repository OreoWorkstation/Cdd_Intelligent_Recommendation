#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/6/3 15:57
# @Author : Kai
# @File : ItemBasedCollaborativeFiltering.py
# @Software: PyCharm

import cdd_mysql
from pyhanlp import *

# recomend similar article
def itemBasedRecommend():
    # load data from database
    dataList = cdd_mysql.loadArticleData()
    ClusterAnalyzer = SafeJClass('com.hankcs.hanlp.mining.cluster.ClusterAnalyzer')
    analyzer = ClusterAnalyzer()
    for id, content in dataList:
        analyzer.addDocument(id, content)

    type_num = 8
    result = analyzer.kmeans(type_num)
    print(result)
    for i in range(type_num):
        for article_id in result[i]:
            cdd_mysql.outputSimilarData(str(article_id), str(i))

if __name__ == "__main__":
    cdd_mysql.clearSimilarTable()
    itemBasedRecommend()
