# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 10:13:41 2018

@author: Harrison
"""

import NewOrder
import NewParamData
#%%新建订单以及参数
def CreateOrder(ordername,modelname,accountid,paramlist):
    data=NewOrder.NewOrder(ordername,modelname,accountid)
    if data ==1:
        try:
            print('建立',modelname,'订单: ',ordername)
            for i in range(paramlist.shape[1]):
                info=NewParamData.NewParamData(paramlist.columns[i],paramlist.iloc[0,i],ordername,modelname,accountid)
                if info==1:
                    print('建立',modelname,'订单: ',ordername,paramlist.columns[i],'=',paramlist.iloc[0,i])
            a='建立 '+modelname+' 订单: '+ordername+' 成功'
        except:
            print('输入有误')    
            a='输入有误'
    return a
if __name__ == '__main__':
    import pandas as pd
    a=['exercise_type','exp_date','init_date','option_type','ref_contract','ref_exchange','ref_underlying','strike']
    data=[['0','2018-06-13','2018-06-13','1','c1901','DCE','c','1820']]
    paramlist=pd.DataFrame(data,columns=a)
    b=CreateOrder('ovo123','ovo','13001',paramlist)