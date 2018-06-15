# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 16:31:25 2018

@author: Jax_GuoSen
"""

from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
import time
from ipywidgets import *
from IPython.display import display,clear_output,display_html
import GetModelParamName
import GetUnderling
import GetContract


global exchange_lst,relation_lst,EN_EX,EN_cont
exchange_lst,relation_lst = GetUnderling.Getunderling()
exchange = exchange_lst['ZHname'].tolist()
exchange.insert(0,'无')
EN_EX = '无'
EN_cont = '无'

#关联3个选项框的函数

def on_select(change):
    global CN_cont_lst,EN_cont_lst,CN_EX,EN_EX
    V2.options = ['无']
    EN_EX = '无'
    for i in range(len(exchange_lst)):
        if change['new'] == exchange_lst.loc[i,'ZHname']:
            CN_cont_lst = relation_lst[i]['ZHname']
            EN_cont_lst = relation_lst[i]['contract']
            CN_EX = exchange_lst.loc[i,'ZHname']
            EN_EX = exchange_lst.loc[i,'exchange']

            tmp = ['无']
            tmp.extend(CN_cont_lst)
            V2.options = tmp

def on_select2(change):
    global EN_cont,CN_cont,cont_date_lst
    V3.options = ['无']
    EN_cont = '无'
    for i in range(len(EN_cont_lst)):
        if change['new'] == CN_cont_lst[i]:
            cont_date_lst = GetContract.GetContract(EN_EX,EN_cont_lst[i])
            tmp = ['无']
            tmp.extend(cont_date_lst)
            V3.options = tmp

            EN_cont = EN_cont_lst[i]
            CN_cont = CN_cont_lst[i]
            #print(EN_cont_lst,CN_EX,EN_EX,CN_cont,EN_cont,cont_date_lst)

def on_select3(change):
    global cont_date
    cont_date = change['new']
    #print(cont_date)

V1 = widgets.Dropdown(options=exchange,description=u'交易所:',disabled=False,continuous_update=True)
V2 = widgets.Dropdown(options=['无'],description=u'品种:',disabled=False,continuous_update=True)
V3 = widgets.Dropdown(options=['无'],description=u'合约:',disabled=False,continuous_update=True)

V1.observe(on_select,'value')
V2.observe(on_select2,'value')
V3.observe(on_select3,'value')


now = datetime.now()
f = now + timedelta(days=90)  #90天后日期
price_date = widgets.DatePicker(
    description='期权报价日:',
    disabled=False,
    value=now.date(),
    tooltip=u'计算期权价格的日期，默认今天'
)

maturity_date = widgets.DatePicker(
    description='期权到期日:',
    disabled=False,
    value=f.date()
)

S = widgets.FloatText(
    value=15000,
    description='标的价格:',
    disabled=False,
    step=1,  #快捷变换间隔
    tooltip=u'待选期权种类'
)



#for each in param_list['paramname']