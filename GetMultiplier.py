# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 08:42:51 2018

@author: Harrison
"""
import OrderManagement.PyMySQLreadZH as PyMySQLreadZH
#%%获取角色列表
def GetMultiplier(exchange,symbol):
    strall="SELECT * FROM futurexdb.underlying where exchange_symbol='"+exchange+"' and underlying_symbol='"+symbol+"';"
    a=PyMySQLreadZH.dbconn(strall)
    return a
#%%使用方法
if __name__ == '__main__':
    a=GetMultiplier('CFFEX','AF')
    idlist1=a.multiplier

