# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 08:40:49 2018

@author: Harrison
"""

import PyMySQLreadZH
#%%获取角色列表
def GetRoleName(accountid):
    strall="SELECT * FROM futurexdb.client_terminal where accountid="+accountid+";"
    a=PyMySQLreadZH.dbconn(strall)
    return a
#%%使用方法
if __name__ == '__main__':
    a=GetRoleName('11001')
    idlist1=a.firstname+a.lastname
    b=GetRoleName('13001')
    idlist2=b.firstname+b.lastname