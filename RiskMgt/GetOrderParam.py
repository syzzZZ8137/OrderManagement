# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 09:32:46 2018

@author: Harrison
"""

import PyMySQLreadZH
def GetOrderParam(accountid,modelinstance):
    strall="SELECT * FROM futurexdb.model_params where accountid='"+accountid+"' and modelinstance='"+modelinstance+"';"
    a=PyMySQLreadZH.dbconn(strall)
    paramlist=a.pivot('modelinstance','paramname','paramstring')
    return paramlist
#%%使用方法
if __name__ == '__main__':
    a=GetOrderParam('13001','oao126')   #查询accountid=13001 订单号为 oao127的参数信息
    a.shape[1]      #获取到的参数个数
    a.columns[0]    #查询第一个参数名
    a.iloc[0,0]     #查询第一个参数值