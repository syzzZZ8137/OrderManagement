# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 09:13:05 2018

@author: Harrison
"""
import PyMySQLwrite
#%% 更改order_record表中的数据，选定accountid,modelinstance以及要更改的参数名
def UpdateOrderStatus(changeitem,changevalue,modelinstance):
    strall="UPDATE `futurexdb`.`order_record_otc` SET `"+changeitem+"`='"+changevalue+"' WHERE `modelinstance`='"+modelinstance+"';"
    data=PyMySQLwrite.MySQLexecute1(strall)                  #调用函数执行MySQL语句
    outputstr='本次更改：'+' '+modelinstance+' '+changeitem+' 值至：'+changevalue+' 受到影响的行数: '+str(data)
    return outputstr                            #返回结果
#%%使用方法
a=UpdateOrderStatus('status','5','oao_13001_11001_1529384719.071866')                
