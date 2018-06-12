# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 16:26:24 2018

@author: Harrison
"""

import PyMySQLreadZH
def GetContract(modelname='ovo'):
    strall="SELECT * FROM futurexdb.modelparamdef where model='"+modelname+"';"
    a=PyMySQLreadZH.dbconn(strall)
    return a

if __name__ == '__main__':
    a=GetContract('ovo')
    sizeparam=a.shape[0]
    for i in range(sizeparam):
        b=a.paramname[i]
        print(b)