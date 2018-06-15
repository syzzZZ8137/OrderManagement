# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 13:23:29 2018

@author: Harrison
"""
import pymysql
#%% MySQL连接函数
def MySQLexecute1(inputstr):                    #替换保存
    connection = pymysql.connect(host='localhost', port=33306, user='localuser', passwd='nodAJe3oY)GO')
    cursor=connection.cursor(pymysql.cursors.DictCursor)
    influencenum=cursor.execute(inputstr)       #受影响条数
    connection.commit()                         #替换保存
    cursor.close()
    connection.close
    return influencenum                         #返回受影响条数