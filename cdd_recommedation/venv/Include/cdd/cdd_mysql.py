#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/5/21 15:12
# @Author : Kai
# @File : cdd_mysql.py
# @Software: PyCharm

import pymysql
import random

# The configuration of connection
connectConfiguration = {
    "host": "scotty.ink",
    "port": 3306,
    "user": "root",
    "passwd": "123456",
    "db": "test",
    "charset": "utf8"
}

# Create Connection Class
class ConnDB():

    def __init__(self, dic):
        self.__conn_dict = dic
        self.conn = None
        self.cursor = None

    def connect(self, cursor=pymysql.cursors.DictCursor):
        self.conn = pymysql.connect(**self.__conn_dict)
        self.cursor = self.conn.cursor(cursor=cursor)
        return self.cursor

    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

# Load data from "t_browse" in order to use them
def loadData():
    connection = ConnDB(connectConfiguration)
    sql = "SELECT * FROM t_browse"
    cursor = connection.connect()
    cursor.execute(sql)
    result = cursor.fetchall()
    # print(result)
    return result
    connection.close()

# Mock function: insert random data into "t_browse"
# This function can be ignored
def initData():
    connection = ConnDB(connectConfiguration)
    cursor = connection.connect()
    sql = "INSERT INTO t_browse (user_id, article_id, browse_value) VALUES(%s, %s, %s)"
    for i in range(100):
        cursor.execute(sql, (random.randint(1, 20), random.randint(1, 30), random.randint(1, 12)))
    connection.close()

# Clear "t_recommend" in order to keep the newest data
def clearTable():
    connection = ConnDB(connectConfiguration)
    cursor = connection.connect()
    cursor.execute("DROP TABLE IF EXISTS t_recommend")
    sql = """CREATE TABLE t_recommend (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `user_id` bigint NOT NULL,
    `article_id` bigint NOT NULL,
    `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci"""
    cursor.execute(sql)
    connection.close()

# Insert data that get from algorithm into "t_recommend"
def outputData(user, article):
    connection = ConnDB(connectConfiguration)
    cursor = connection.connect()
    sql = "INSERT INTO t_recommend (user_id, article_id) VALUES(%s, %s)"
    # For test, need to change
    # for i in range(10):
    #     cursor.execute(sql, (random.randint(1, 20), random.randint(1, 30)))\
    cursor.execute(sql, (user, article))
    connection.close()

# initData()
# loadData()
# print('*'*40)
# clearTable()
# outputData()