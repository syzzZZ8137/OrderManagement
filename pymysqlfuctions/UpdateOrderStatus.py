# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 09:13:05 2018

@author: Harrison
"""
import PyMySQLwrite
#%% 更改order_record表中的数据，选定accountid,modelinstance以及要更改的参数名
def UpdateOrderStatus(changeitem,changevalue,accountid,modelinstance):
    strall="UPDATE `futurexdb`.`order_record_otc` SET `"+changeitem+"`='"+changevalue+"' WHERE `accountid`='"+accountid+"' and`modelinstance`='"+modelinstance+"';"
    data=PyMySQLwrite.MySQLexecute1(strall)                  #调用函数执行MySQL语句
    outputstr='本次更改：'+accountid+' '+modelinstance+' '+changeitem+' 值至：'+changevalue+' 受到影响的行数: '+str(data)
    return outputstr                            #返回结果
#%%使用方法
    #a=UpdateOrderStatus('status','1','13001','oao-test-1')               #RiskManager 确认订单或Sales 预取消订单
    #a=UpdateOrderStatus('quantity_filled','1','13001','ovo124')          #trader完成订单对冲
