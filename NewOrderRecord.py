# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 14:01:59 2018

@author: Harrison
"""
import OrderManagement.PyMySQLwrite as PyMySQLwrite
#%%新建下单订单
def NewOrderRecord(infolist):  #输入需要建立的订单，名字，模型
    strall="INSERT INTO `futurexdb`.`order_record_otc` (`"
    str1=''
    str2=''
    for i in range(infolist.shape[1]):
        str1=str1+infolist.columns[i]+'`,`'
        str2=str2+"'"+str(infolist.iloc[0,i])+"',"
    strall=strall+str1[:-2]+') VALUES ('+str2[:-1]+');'
    data=PyMySQLwrite.MySQLexecute1(strall)  
    return data
#%%使用方法
if __name__ == '__main__':
    import pandas as pd
    import CreateOrder
    ordername='oao127'
    accountid='13001'
    modelname='oao'
    a=['exercise_type','exp_date','init_date','option_type','ref_contract','ref_exchange','ref_underlying','strike']
    data=[['0','2018-06-13','2018-06-13','1','c1901','DCE','c','1820']]
    paramlist=pd.DataFrame(data,columns=a)
    b=CreateOrder.CreateOrder(ordername,modelname,accountid,paramlist)
    print(b)
    
    c=['accountid', 'modelinstance', 'customerid', 'riskid', 'price', 'quantity', 'quantity_filled', 'is_buy', 'is_open', 'exec_type', 'tif', 'status', 'trading_type', 'tradingday', 'errorcode']
    d=[[accountid,ordername,'11001','14001','1234','16','0','1','1','9','0','14','0','2018-09-01','0']]
    infolist=pd.DataFrame(d,columns=c)
    e=NewOrderRecord(infolist)         
    print(e)

