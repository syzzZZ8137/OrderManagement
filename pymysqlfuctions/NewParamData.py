# -*- coding: utf-8 -*-
"""
Created on Thu May 31 13:42:04 2018

@author: Harrison
"""
import PyMySQLwrite
#%% 向model_params表，为选定合约代码输入参数
def NewParamData(itemname,itemvalue,modelinstance,modelname,accountid):
    strall="INSERT INTO `futurexdb`.`model_params` (`accountid`, `modelinstance`, `model`, `paramname`, `paramstring`) VALUES ('"+accountid+"',"\
    + "'"+modelinstance+"'"+", '"+modelname+"', '"+itemname+"', '"+itemvalue+"')"
    data=PyMySQLwrite.MySQLexecute1(strall)  
    return data

if __name__ == '__main__':
    import GetModelParamName
    modelname='ovo'
    modelinstance='ovo-1000'
    a=GetModelParamName.GetContract('ovo')
    sizeparam=a.shape[0]
    for i in range(sizeparam):
        b=a.paramname[i]
        a=NewParamData(b,'alistofdata',modelinstance,modelname)
        print(a)