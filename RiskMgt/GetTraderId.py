# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 12:58:55 2018

@author: Harrison
"""
import PyMySQLreadZH
import GetRoletype
import pandas as pd
def GetSlaveId(masterid): #获取管辖下的Id
    strall="SELECT * FROM futurexdb.accountid_map where master_id='"+masterid+"';"
    a=PyMySQLreadZH.dbconn(strall)
    return a
def GetTraderId(masterid):#判断是否为Trader
    b=GetSlaveId(masterid)
    c=b.slave_id
    traderlist=GetRoletype.GetRoleType('12')
    a= pd.DataFrame()
    for i in range(len(c)): 
        a=a.append(traderlist[traderlist['accountid']==c[i]])
    return a
#%%使用方法
if __name__ == '__main__':
    a=GetTraderId('14001')
    
