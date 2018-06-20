# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 13:47:33 2018

@author: Jax_GuoSen
"""

import PyMySQLreadZH
#%%获取角色列表
def GetRiskList():
    strall="SELECT * FROM futurexdb.client_terminal where roletype=14;"
    a=PyMySQLreadZH.dbconn(strall)
    
    return a

def GetOrder(riskid):
    strall="SELECT * FROM futurexdb.order_record_otc where  riskid ='"+riskid+"';"
    try:
        a = PyMySQLreadZH.dbconn(strall)
    except:
        a = 0
    
    return a


#%%使用方法
if __name__ == '__main__':
    a=GetRiskList()
    a = a['accountid'].tolist()
    
    b=GetOrder(str(a[0]))