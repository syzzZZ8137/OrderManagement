# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 16:57:34 2018

@author: Harrison
"""

import PyMySQLreadZH
#%%获取角色列表
def GetOrderList(accountid):
    strall="SELECT * FROM futurexdb.order_record_otc where  accountid ='"+accountid+"';"
    a=PyMySQLreadZH.dbconn(strall)
    return a
#%%使用方法
if __name__ == '__main__':
    a=GetOrderList('13001')
    idlist1=a.modelinstance
    b=GetOrderList('13002')
    idlist2=b.modelinstance