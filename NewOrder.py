# -*- coding: utf-8 -*-
"""
Created on Thu May 31 14:15:39 2018

@author: Harrison
"""
import OrderManagement.PyMySQLwrite as PyMySQLwrite
#%% 在usermodels表里建立新合约
def NewOrder(modelinstance,modelname,accountid):  #输入需要建立的订单，名字，模型
    strall="INSERT INTO `futurexdb`.`usermodels` (`accountid`, `modelinstance`, `model`) VALUES ('"+accountid+"', '"+modelinstance+"', '"+modelname+"');"
    data=PyMySQLwrite.MySQLexecute1(strall)  
    return data