# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 10:40:14 2018

@author: Harrison
"""

import PyMySQLwrite
#%% 删除合约以及全部参数值
def DelOrder(model,order,accountid):
    strall="DELETE FROM `futurexdb`.`usermodels` WHERE `accountid`='"+accountid+"' and `model`='"+model+"'and`modelinstance`='"+order+"';"
    data=PyMySQLwrite.MySQLexecute1(strall)  
    return data