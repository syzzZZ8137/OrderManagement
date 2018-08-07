# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 13:26:21 2018

@author: Jax_GuoSen
"""

import GetOrderList
import GetOrderParam
import UpdateOrderStatus
import GetRiskList
import GetRoleName
import GetTraderId
import GetPoSymbol
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import *
from pandastable import Table, TableModel
import pandas as pd

def update(p):
    table.clearTable()
    Login_RskMgt(p)

def Login_RskMgt(p):
    global res,table,trader
    res = GetRiskList.GetOrder(str(RskChosen.get()))
    
    if type(res) == int:
        res_disp = pd.DataFrame()
        #说明提取数据时报错
    else:
        res = res[res['status'].isin([1,3,5,6,14])]
        OrderID['values'] =  res[res['status'].isin([14])]['modelinstance'].tolist()
        OrderID2['values'] =  res[res['status'].isin([1])]['modelinstance'].tolist()
        
        a = [14,1,5,3]
        #print(111,is_disp)
        disp = [x for x in range(len(is_disp)) if is_disp[x] == 1]
        #print(222,disp)
        a = [a[x] for x in disp]
        #print(333,a)
        res = res[res['status'].isin(a)]
        
        trader = GetTraderId.GetTraderId(str(RskChosen.get()))
        trader1 = trader['accountid'].apply(lambda x : str(x)+'-')
        trader1 = trader1+trader['firstname']+trader['lastname']
        TraderChosen['values'] = trader1.tolist()
        res.reset_index(inplace=True,drop=True)
        
        
        res2 = pd.DataFrame()
                    
        for i in range(len(res)):
            
            tmp = GetOrderParam.GetOrderParam(str(res.loc[i,'accountid']),res.loc[i,'modelinstance'])
            res2 = res2.append(tmp)
        
        
        res_disp = pd.DataFrame()
        
        for i in range(len(res)):
            each = res.loc[i,'modelinstance']
            res_disp.loc[i,'订单号'] = each
            
            res_disp.loc[i,'客户ID'] = int(res.loc[i,'customerid'])
            client = GetRoleName.GetRoleName(str(res_disp.loc[i,'客户ID']))
            client = client['firstname'].values[0]+client['lastname'].values[0]
            res_disp.loc[i,'客户姓名'] = client
            
            res_disp.loc[i,'业务员ID'] = int(res.loc[i,'accountid'])
            sales = GetRoleName.GetRoleName(str(res_disp.loc[i,'业务员ID']))
            sales = sales['firstname'].values[0]+sales['lastname'].values[0]
            res_disp.loc[i,'业务员姓名'] = sales
            #res_disp.loc[i,'订单状态'] = res.loc[each,'status']
            res_disp.loc[i,'已分配交易员'] = res.loc[i,'traderid']
            res_disp.loc[i,'已分配组合'] = res.loc[i,'portfolio_symbol']
            
            if res.loc[i,'status'] == 14:
                res_disp.loc[i,'状态'] = '下单成功,等待审阅'
            elif res.loc[i,'status'] == 6:
                res_disp.loc[i,'状态'] = '正在审阅'
            elif res.loc[i,'status'] == 1:
                res_disp.loc[i,'状态'] = '已通过审阅'
            elif res.loc[i,'status'] == 5:
                res_disp.loc[i,'状态'] = '未通过审阅'
            elif res.loc[i,'status'] == 3:
                res_disp.loc[i,'状态'] = '已撤单'
            else:
                pass
            
            res_disp.loc[i,'交易所'] = res2.loc[each,'ref_exchange']
            res_disp.loc[i,'品种'] = res2.loc[each,'ref_underlying']
            res_disp.loc[i,'合约'] = res2.loc[each,'ref_contract']
            res_disp.loc[i,'期权报价日'] = res2.loc[each,'init_date']
            res_disp.loc[i,'期权到期日'] = res2.loc[each,'exp_date']
            if 'sett_start_date' in res2.columns.tolist():
                res_disp.loc[i,'期权起均日'] = res2.loc[each,'sett_start_date']
            if 'sett_end_date' in res2.columns.tolist():
                res_disp.loc[i,'期权终均日'] = res2.loc[each,'sett_end_date']
            res_disp.loc[i,'行权方式'] = '欧式(European)' if res2.loc[each,'exercise_type']=='0' else '美式(American)'
            res_disp.loc[i,'期权类型'] = '看涨(Call)' if res2.loc[each,'option_type']=='0' else '看跌(Put)'
            if each[:3] == 'oao':
                res_disp.loc[i,'期权类型'] = '亚式(Asian)'+res_disp.loc[i,'期权类型']
            elif each[:3] == 'ovo':
                res_disp.loc[i,'期权类型'] = '香草(Vanilla)'+res_disp.loc[i,'期权类型']
            else:
                pass
            res_disp.loc[i,'客户备注'] = res.loc[i,'description']
            res_disp.loc[i,'销售期权单价'] = res.loc[i,'price']
            res_disp.loc[i,'理论期权单价'] = res.loc[i,'theo_price']
            res_disp.loc[i,'销售波动率'] = res.loc[i,'theo_volatility']
            res_disp.loc[i,'销售期权总价'] = res.loc[i,'total_premium']
            res_disp.loc[i,'销售标的价格'] = res.loc[i,'underlying_price']
            res_disp.loc[i,'销售无风险利率'] = res.loc[i,'riskfree_rate']
            
            res_disp.loc[i,'行权价'] = res2.loc[each,'strike']
            res_disp.loc[i,'期权手数'] = res.loc[i,'quantity']
            res_disp.loc[i,'方向'] = '买入' if res.loc[i,'is_buy']==1 else '卖出'
            
            res_disp = res_disp.sort_values('状态')
          
    former_labelframe = labelframe.pack_slaves()
    for each in former_labelframe:
        each.destroy()
        
    f = Frame(labelframe,width=300)
    f.pack(fill='both')
    
    table = pt = Table(f, dataframe=res_disp,width=1700)

    #table.grid(row=1,column=1,rowspan=5,columnspan=2)
    table.show()

def Get_Portfolio(p):
    traderID = str(TraderChosen.get()).split('-')[0]
    ps = GetPoSymbol.GetPoSymbol(traderID)
    ps = ps['portfolio_symbol'].tolist()
    PortfolioChosen['values'] = ps
    PortfolioChosen.current(0)
    
def RiskJudge(signal,OrderID):
    isdo = tk.messagebox.askokcancel('Validation', '要执行此操作吗')
    #print(isdo)
    if isdo:
        if type(res) == int:
            #对应风控官没用业务数据
            tk.messagebox.showerror('Status Update','Empty Account')
        
        else:
            
            if signal == 0:
                if res[res['modelinstance']==OrderID.get()]['status'].values[0] == 14:
                    a = UpdateOrderStatus.UpdateOrderStatus('status','5',OrderID.get())
                else:
                    tk.messagebox.showinfo('Status Update','Invalid Action1')
            
                if a[-1] == '0':
                    tk.messagebox.showinfo('Status Update','Invalid Action2')
                else:
                    tk.messagebox.showinfo('Status Update','Rejected Successfully!')
            elif signal == 1:
                #Approval
                if res[res['modelinstance']==OrderID.get()]['status'].values[0] == 14:
                    a = UpdateOrderStatus.UpdateOrderStatus('status','1',OrderID.get())
                else:
                    tk.messagebox.showinfo('Status Update','Invalid Action3')
                if a[-1] == '0':
                    tk.messagebox.showinfo('Status Update','Invalid Action4')
                else:
                    tk.messagebox.showinfo('Status Update','Approval Successfully!')
                    
            else:
                tk.messagebox.showinfo('Status Update','Invalid Code')


def distribute_trader(p):
    b = UpdateOrderStatus.UpdateOrderStatus('traderid',str(TraderChosen.get()).split('-')[0],OrderID2.get())
    c = UpdateOrderStatus.UpdateOrderStatus('portfolio_symbol',PortfolioChosen.get(),OrderID2.get())
    tk.messagebox.showinfo('Trader Portfolio Distribute','Distribute Successfully!')


def selection():
    global is_disp
    is_disp = []
    for i in range(len(var_lst)):
        is_disp.append(var_lst[i].get())
    #print(is_disp)


root = Tk() 
root.title('国信期货场外期权订单管理系统（后台）')  

labelframe = LabelFrame(root, text='OrderListTable')
labelframe.pack(fill='y')


RiskID = GetRiskList.GetRiskList()
RiskID = RiskID['accountid'].tolist()

global RskChosen,OrderID,TraderChosen,PortfolioChosen,OrderID2,is_disp
labelframe1 = LabelFrame(root, text='RiskManagerID')
labelframe1.pack(fill='y')


RskChosen = ttk.Combobox(labelframe1, width=12)
RskChosen['values'] =  RiskID

RskChosen.pack(fill='both')
RskChosen.bind("<<ComboboxSelected>>",Login_RskMgt)

button_bg = '#D5E0EE'  
button_active_bg = '#E5E35B'

#checkbutton
var_lst = []
is_disp = [1,0,0,0]
status = ['下单成功,等待审阅','已通过审阅','未通过审阅','已撤单']
l4 = LabelFrame(labelframe1, text='Display')
l4.pack(fill='both')
for each in status:
    var = tk.IntVar()
    checkbt = Checkbutton(l4,text=each,\
                          variable=var, onvalue=1, offvalue=0,\
                          command=selection)
    checkbt.pack(fill='both',side='left')
    if each == '下单成功,等待审阅':
        checkbt.select()
    var_lst.append(var)



bt1 = Button(labelframe1,text='Update Data',bg=button_bg, padx=50, pady=3,fg='blue',\
           command=lambda : update(0),activebackground = button_active_bg,\
           font = tkFont.Font(size=12, weight=tkFont.BOLD))
bt1.pack(fill='both')


l = LabelFrame(root, text='Order')
l.pack(fill='y')

l1 = LabelFrame(l, text='Order')
l1.pack(fill='y')
OrderID = ttk.Combobox(l1, width=40)
OrderID.pack(fill='both')

bt = Button(l,text='Approval',bg=button_bg, padx=50, pady=3,fg='red',\
           command=lambda : RiskJudge(1,OrderID),activebackground = button_active_bg,\
           font = tkFont.Font(size=12, weight=tkFont.BOLD))

bt.pack(fill='both')


bt = Button(l,text='Reject',bg=button_bg, padx=50, pady=3,fg='green',\
           command=lambda : RiskJudge(0,OrderID),activebackground = button_active_bg,\
           font = tkFont.Font(size=12, weight=tkFont.BOLD))
bt.pack(fill='both')


ll = LabelFrame(root, text='Trader-Portfolio')
ll.pack(fill='y')

ll1 = LabelFrame(ll, text='OrderID')
ll1.pack(fill='y')
OrderID2 = ttk.Combobox(ll1, width=40)
OrderID2.pack(fill='both')

l2 = LabelFrame(ll, text='Trader')
l2.pack(fill='y')
TraderChosen = ttk.Combobox(l2, width=40)
TraderChosen.pack(fill='both')
TraderChosen.bind("<<ComboboxSelected>>",Get_Portfolio)


l3 = LabelFrame(ll, text='Portfolio')
l3.pack(fill='y')
PortfolioChosen = ttk.Combobox(l3, width=40)
PortfolioChosen.pack(fill='both')

bt = Button(ll,text='Distribute',bg=button_bg, padx=50, pady=3,fg='red',\
           command=lambda : distribute_trader(0),activebackground = button_active_bg,\
           font = tkFont.Font(size=12, weight=tkFont.BOLD))
bt.pack(fill='both')




root.mainloop()


