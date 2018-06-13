# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 14:01:59 2018

@author: Harrison
"""
import PyMySQLwrite
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
    a=['accountid', 'modelinstance', 'customerid', 'riskid', 'price', 'quantity', 'quantity_filled', 'is_buy', 'is_open', 'exec_type', 'tif', 'status', 'trading_type', 'tradingday', 'errorcode']
    data=[['13001','ovo20180613102201','11001','14001','1234','16','0','1','1','9','0','14','0','2018-09-01','0']]
    infolist=pd.DataFrame(data,columns=a)
    b=NewOrderRecord(infolist)            

