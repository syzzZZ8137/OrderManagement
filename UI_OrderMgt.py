from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
import time
from ipywidgets import *
from IPython.display import display,clear_output,display_html
import OrderManagement.GetModelParamName as GetModelParamName
import OrderManagement.GetUnderling as GetUnderling
import OrderManagement.GetContract as GetContract
import OrderManagement.GetRoletype as GetRoletype
import OrderManagement.CreateOrder as CreateOrder
import OrderManagement.NewOrderRecord as NewOrderRecord
import OrderManagement.GetOrderList as GetOrderList
import OrderManagement.GetOrderParam as GetOrderParam
import OrderManagement.UpdateOrderStatus as UpdateOrderStatus
import OrderManagement.GetMultiplier as GetMultiplier
import OrderManagement.Option_Portfolio as OP
import OrderManagement.MC_Asian_Pricer as MC

#%%
#香草期权
def on_btn_ovo_clicked(p):
    customer_data = GetRoletype.GetRoleType('11')
    sales_data = GetRoletype.GetRoleType('13')
    
    customer_id = list(customer_data['accountid'])
    customer_id.insert(0,'无')
    sales_id = list(sales_data['accountid'])
    sales_id.insert(0,'无')
    
    customer = widgets.Dropdown(options=customer_id,description=u'客户ID:',disabled=False,continuous_update=True)
    sales = widgets.Dropdown(options=sales_id,description=u'业务员ID:',disabled=False,continuous_update=True) 
    
    global exchange_lst,relation_lst,EN_EX,EN_cont,cont_date
    exchange_lst,relation_lst = GetUnderling.Getunderling()
    exchange = exchange_lst['ZHname'].tolist()
    exchange.insert(0,'无')
    EN_EX = '无'
    EN_cont = '无'
    cont_date = '无'
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
    
    
    clear_output()
    now = datetime.now()
    f = now + timedelta(days=90)  #90天后日期
    price_date = widgets.DatePicker(
        description='期权发行日:',
        disabled=False,
        value=now.date(),
        tooltip=u'计算期权价格的日期，默认今天'
    )

    maturity_date = widgets.DatePicker(
        description='期权到期日:',
        disabled=False,
        value=f.date()
    )
    
    option_type = widgets.Dropdown(
        options=['看涨(Call)',
                 '看跌(Put)'],
        value='看涨(Call)',
        description=u'期权类型:',
        disabled=False,
        continuous_update=True,
    )
    
    exercise_type = widgets.Dropdown(
        options=['欧式(European)',
                 '美式(American)'],
        value='欧式(European)',
        description=u'行权方式:',
        disabled=False,
        continuous_update=True,
    )
    
    option_price = widgets.BoundedFloatText(
        description='期权单价:',
        disabled=False,
        step=1,
        min=0,
        max=1000000000
    )
    
    strike = widgets.BoundedFloatText(
        description='行权价:',
        disabled=False,
        step=1,
        min=0,
        max=1000000000
    )
    
    quantity= widgets.BoundedIntText(
        description='期权手数:',
        disabled=False,
        step=1,
        min=0,
        max=1000000000
    )
    
    direction = widgets.ToggleButtons(
        options=['买入', '卖出'],
        description='方向:',
        disabled=False,
        button_style='info', # 'success', 'info', 'warning', 'danger' or ''
        value = '买入'
    )
    
    btn_init = widgets.Button(
        description=u'重置',
        disabled=False,
        button_style='success', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击返回上一单元',
        icon='check'
    )
    
    btn_submit = widgets.Button(
        description=u'提交',
        disabled=False,
        button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'提交订单',
        icon='check'
    )
    
    S = widgets.FloatText(
        description='标的价格:',
        disabled=False,
        step=1,  #快捷变换间隔

    )
    
    r = widgets.FloatText(
        value=1,
        disabled=False,
        step=0.01,
        layout=Layout(width='207.5px')
    )
    Labelr = widgets.Label(value='无风险利率(%):')
    Boxr = widgets.HBox([Labelr,r])
    
    vol= widgets.BoundedFloatText(
        description='波动率(%):',
        disabled=False,
        step=1,
        min=0,
        max=1000000000
    )
    
    info_id = widgets.HBox([customer,sales])
    info0 = widgets.HBox([V1,V2,V3])
    info1 = widgets.HBox([price_date,maturity_date])
    info2 = widgets.HBox([exercise_type,option_type])
    info3 = widgets.HBox([option_price])
    info33 = widgets.HBox([S,strike])
    info333 = widgets.HBox([vol,Boxr])
    info4 = widgets.HBox([quantity,direction])
    
    global order_info
    order_info = widgets.VBox([info_id,info0,info1,info2,info3,info33,info333,info4])
    
    
    def submit(p):
        clear_output()
        display(order_info)
        select = widgets.HBox([btn_submit,btn_init])
        display(select)
        
        if EN_EX == '无':
            print('请选择交易所')
        elif EN_cont == '无':
            print('请选择标的资产')
        elif cont_date == '无':
            print('请选择合约')
        elif option_price.value == 0:
            print('请输入期权单价')
        elif strike.value == 0 :
            print('请输入行权价')
        elif S.value == 0:
            print('请输入标的价格')
        elif vol.value == 0:
            print('请输入波动率')
        elif quantity.value == 0:
            print('请输入期权手数')
        elif customer.value=='无':
            print('请选择客户ID')
        elif sales.value=='无':
            print('请选择业务员ID')
        elif price_date.value>=maturity_date.value:
            print('请保证期权发行日在到期日之前')
        else:
            op_t = 0 if option_type.value == '看涨(Call)' else 1
            ex_t = 0 if exercise_type.value == '欧式(European)' else 1
            is_buy = 1 if direction.value == '买入' else 0
            
            column = ['exercise_type','exp_date','init_date','option_type','ref_contract',\
                      'ref_exchange','ref_underlying','strike']
            data = [[str(ex_t),str(maturity_date.value),str(price_date.value),str(op_t),\
                     cont_date,EN_EX,EN_cont,str(strike.value)]]
            paramlist=pd.DataFrame(data,columns=column)
            order_id = 'ovo_'+'%d_'%sales.value+'%d_'%customer.value+'%s'%str(time.time())
            #生成订单，命名规则为：期权种类_salesID_customerID_时间
            a = CreateOrder.CreateOrder(order_id,'ovo',str(sales.value),paramlist) 
            #print(a)
            
            multiplier = GetMultiplier.GetMultiplier(EN_EX,EN_cont)
            multiplier = multiplier['multiplier'].values[0]
            total_premium = option_price.value*multiplier
            
            theo_price = 0
            tp = exercise_type.value[:2]+'/'+option_type.value[:2]
            market_property = {'underlying price':S.value,'interest':r.value/100,\
                               'volatility':vol.value/100,'dividend':0}
            option_property = {'type':tp,'position':1,\
                               'strike':strike.value,'maturity':((maturity_date.value - price_date.value).days+1)/365}
            
            theo_price = OP.BS_formula(market_property,option_property)
            
            
            
            
            column2 = ['accountid', 'modelinstance', 'customerid', 'riskid', 'price', 'quantity',\
                       'is_buy', 'exec_type', 'status','quantity_filled', 'is_open',\
                        'tif', 'trading_type', 'tradingday', 'errorcode',\
                        'theo_volatility','theo_price','total_premium',\
                        'underlying_price','riskfree_rate']
            data2 = [[str(sales.value),order_id,'%d'%customer.value,'14001',str(option_price.value),str(quantity.value),\
                      str(is_buy),'9','14','0','0',\
                      '0','0',str(price_date.value),'0',str(vol.value/100),str(theo_price),str(total_premium),\
                      str(S.value),str(r.value/100)]]
            infolist = pd.DataFrame(data2,columns=column2)
            b = NewOrderRecord.NewOrderRecord(infolist)          
            
            column_disp = ['客户ID','业务员ID','交易所','品种','合约','期权发行日','期权到期日',\
                           '行权方式','期权类型','期权单价',\
                           '行权价','期权手数','方向']
            data_disp = [[customer.value,sales.value,EN_EX,EN_cont,cont_date,price_date.value,maturity_date.value,\
                        exercise_type.value,option_type.value,option_price.value,\
                        strike.value,quantity.value,direction.value]]
            df_disp=pd.DataFrame(data_disp,columns=column_disp)
            print('提交完成，您提交的信息如下：')
            print('您的订单号为%s'%order_id)
            display(df_disp)
    
    def init(p):
        display_()
    
    btn_init.on_click(init)
    btn_submit.on_click(submit)
    
    display(order_info)
    select = widgets.HBox([btn_submit,btn_init])
    display(select)
    
    
    
#%%
#亚式期权
def on_btn_oao_clicked(p):
    customer_data = GetRoletype.GetRoleType('11')
    sales_data = GetRoletype.GetRoleType('13')
    
    customer_id = list(customer_data['accountid'])
    customer_id.insert(0,'无')
    sales_id = list(sales_data['accountid'])
    sales_id.insert(0,'无')
    
    customer = widgets.Dropdown(options=customer_id,description=u'客户ID:',disabled=False,continuous_update=True)
    sales = widgets.Dropdown(options=sales_id,description=u'业务员ID:',disabled=False,continuous_update=True) 
    
    global exchange_lst,relation_lst,EN_EX,EN_cont,cont_date
    exchange_lst,relation_lst = GetUnderling.Getunderling()
    exchange = exchange_lst['ZHname'].tolist()
    exchange.insert(0,'无')
    EN_EX = '无'
    EN_cont = '无'
    cont_date = '无'
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
    
    clear_output()
    now = datetime.now()
    f = now + timedelta(days=90)  #90天后日期
    price_date = widgets.DatePicker(
        description='期权发行日:',
        disabled=False,
        value=now.date()
    )

    start_fixed_date = widgets.DatePicker(
        description='期权起均日:',
        disabled=False,
        value=now.date()
    )
    end_fixed_date = widgets.DatePicker(
        description='期权终均日:',
        disabled=False,
        value=f.date()
    )
    
    maturity_date = widgets.DatePicker(
        description='期权到期日:',
        disabled=False,
        value=f.date()
    )
    
    option_type = widgets.Dropdown(
        options=['看涨(Call)',
                 '看跌(Put)'],
        value='看涨(Call)',
        description=u'期权类型:',
        disabled=False,
        continuous_update=True,
    )
    
    exercise_type = widgets.Dropdown(
        options=['欧式(European)',
                 '美式(American)'],
        value='欧式(European)',
        description=u'行权方式:',
        disabled=False,
        continuous_update=True,
    )
    
    option_price = widgets.BoundedFloatText(
        description='期权单价:',
        disabled=False,
        step=1,
        min=0,
        max=1000000000
    )
    
    strike = widgets.BoundedFloatText(
        description='行权价:',
        disabled=False,
        step=1,
        min=0,
        max=1000000000
    )
    
    quantity= widgets.BoundedFloatText(
        description='期权手数:',
        disabled=False,
        step=1,
        min=0,
        max=1000000000
    )
    
    vol= widgets.BoundedFloatText(
        description='波动率(%):',
        disabled=False,
        step=1,
        min=0,
        max=1000000000
    )
    
    direction = widgets.ToggleButtons(
        options=['买入', '卖出'],
        description='方向:',
        disabled=False,
        button_style='info', # 'success', 'info', 'warning', 'danger' or ''
        value = '买入'
    )
    
    btn_init = widgets.Button(
        description=u'重置',
        disabled=False,
        button_style='success', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击返回上一单元',
        icon='check'
    )
    
    btn_submit = widgets.Button(
        description=u'提交',
        disabled=False,
        button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'提交订单',
        icon='check'
    )
    
    S = widgets.FloatText(
        description='标的价格:',
        disabled=False,
        step=1,  #快捷变换间隔

    )
    
    r = widgets.FloatText(
        value=1,
        disabled=False,
        step=0.01,
        layout=Layout(width='207.5px')
    )
    Labelr = widgets.Label(value='无风险利率(%):')
    Boxr = widgets.HBox([Labelr,r])
    
    info_id = widgets.HBox([customer,sales])
    info0 = widgets.HBox([V1,V2,V3])
    info1 = widgets.HBox([price_date,maturity_date])
    info11 = widgets.HBox([start_fixed_date,end_fixed_date])
    info2 = widgets.HBox([exercise_type,option_type])
    info3 = widgets.HBox([option_price])
    info33 = widgets.HBox([S,strike])
    info333 = widgets.HBox([vol,Boxr])
    info4 = widgets.HBox([quantity,direction])
    
    global order_info
    order_info = widgets.VBox([info_id,info0,info1,info11,info2,info3,info33,info333,info4])
    
    
    def submit(p):
        clear_output()
        display(order_info)
        select = widgets.HBox([btn_submit,btn_init])
        display(select)
        
        if EN_EX == '无':
            print('请选择交易所')
        elif EN_cont == '无':
            print('请选择标的资产')
        elif cont_date == '无':
            print('请选择合约')
        elif option_price.value == 0:
            print('请输入期权单价')
        elif S.value == 0:
            print('请输入标的价格')
        elif vol.value == 0:
            print('请输入波动率')
        elif strike.value == 0 :
            print('请输入行权价')
        elif quantity.value == 0:
            print('请输入期权手数')
        elif customer.value=='无':
            print('请选择客户ID')
        elif sales.value=='无':
            print('请选择业务员ID')
        elif price_date.value>=maturity_date.value:
            print('请保证期权发行日在到期日之前')
        elif price_date.value>start_fixed_date.value:
            print('请保证期权发行日在起均日之前')
        elif start_fixed_date.value>=end_fixed_date.value:
            print('请保证期权起均日在终均日之前')
            
        else:
            print('下单中，请稍后！')
            op_t = 0 if option_type.value == '看涨(Call)' else 1
            ex_t = 0 if exercise_type.value == '欧式(European)' else 1
            is_buy = 1 if direction.value == '买入' else 0
            
            column = ['exercise_type','exp_date','init_date','option_type','ref_contract',\
                      'ref_exchange','ref_underlying','strike','sett_start_date','sett_end_date']
            data = [[str(ex_t),str(maturity_date.value),str(price_date.value),str(op_t),\
                     cont_date,EN_EX,EN_cont,str(strike.value),str(start_fixed_date.value),str(end_fixed_date.value)]]
            paramlist=pd.DataFrame(data,columns=column)
            order_id = 'oao_'+'%d_'%sales.value+'%d_'%customer.value+'%s'%str(time.time())
            #生成订单，命名规则为：期权种类_salesID_customerID_时间
            a = CreateOrder.CreateOrder(order_id,'oao',str(sales.value),paramlist) 
            #print(a)
            
            column2 = ['accountid', 'modelinstance', 'customerid', 'riskid', 'price', 'quantity',\
                       'is_buy', 'exec_type', 'status','quantity_filled', 'is_open',\
                        'tif', 'trading_type', 'tradingday', 'errorcode','theo_volatility','theo_price','total_premium',\
                        'underlying_price','riskfree_rate']
            
            #亚式期权回算
            SA = S.value
            q = 0
            Nsamples = 50000
            Tsamples = (maturity_date.value-price_date.value).days*10
            theo_price = 0
            
            if option_type.value == '看涨(Call)':
                OT = '亚式/算术平均/看涨/固定'
            else:
                OT = '亚式/算术平均/看跌/固定'
                
            Ta,Tb,Tc,sit = MC.time_split(price_date.value,start_fixed_date.value,end_fixed_date.value,maturity_date.value)
            if Ta<=0:
                print('输入有误！请确认到期日在报价日之后！')
            elif Tb<0:
                print('输入有误！请确认到期日在起均日之后！')
            elif Tc<0:
                print('输入有误！请确认到期日在终均日之后！')
            elif Tb<Tc:
                print('输入有误！请确认终均日在起均日之后！')
            else:
                if sit==1:
                    random = MC.random_gen(Nsamples,Tsamples)
                    theo_price,se = MC.Asian_Disc_MC(random,S.value,strike.value,Ta,Tb,Tc,sit,r.value/100,vol.value/100,q,SA,
                                         OT,Nsamples,Tsamples)
                    
                    
                else:
                    print('输入有误！请确认起均日在报价日之后！')
                
            multiplier = GetMultiplier.GetMultiplier(EN_EX,EN_cont)
            multiplier = multiplier['multiplier'].values[0]
            total_premium = option_price.value*multiplier
            
            data2 = [[str(sales.value),order_id,'%d'%customer.value,'14001',str(option_price.value),str(quantity.value),\
                      str(is_buy),'9','14','0','0',\
                      '0','0',str(price_date.value),'0',\
                      '%f'%(vol.value/100),str(theo_price),str(total_premium),str(S.value),str(r.value/100)]]
            infolist = pd.DataFrame(data2,columns=column2)
            b = NewOrderRecord.NewOrderRecord(infolist)          
            
            column_disp = ['客户ID','业务员ID','交易所','品种','合约','期权报价日','期权到期日',\
                           '期权起均日','期权终均日','行权方式','期权类型','期权单价',\
                           '行权价','期权手数','方向']
            data_disp = [[customer.value,sales.value,EN_EX,EN_cont,cont_date,price_date.value,maturity_date.value,\
                        start_fixed_date.value,end_fixed_date.value,exercise_type.value,option_type.value,option_price.value,\
                        strike.value,quantity.value,direction.value]]
            df_disp=pd.DataFrame(data_disp,columns=column_disp)
            print('提交完成，您提交的信息如下：')
            print('您的订单号为%s'%order_id)
            display(df_disp)
    
    def init(p):
        display_()
        
    btn_init.on_click(init)
    btn_submit.on_click(submit)
    
    display(order_info)
    select = widgets.HBox([btn_submit,btn_init])
    display(select)

def on_btn_qw_clicked(p):
    
    clear_output()
    
    sales_data = GetRoletype.GetRoleType('13')
    sales_id = list(sales_data['accountid'])
    sales_id.insert(0,'无')
    
    
    global sales
    sales = widgets.Dropdown(options=sales_id,description=u'业务员ID:',disabled=False,continuous_update=True) 
    
    btn_init = widgets.Button(
        description=u'重置',
        disabled=False,
        button_style='success', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击返回上一单元',
        icon='check'
    )
    
    btn_query = widgets.Button(
        description=u'查询',
        disabled=False,
        button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击查询已提交订单',
        icon='check'
    )
    
    btn_withdrawl = widgets.Button(
        description=u'撤单',
        disabled=False,
        button_style='info', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击撤单',
        icon='check'
    )
    
    global withdrawl_order_id
    withdrawl_order_id = widgets.Text(description='撤单号',layout=Layout(width='450px'))   
    
    
    def query_click(p):
        clear_output()
        display(sales,withdrawl_order_id,select)
        if sales.value=='无':
            print('请选择业务员ID')
        else:
            print('您选择的业务员ID为：',sales.value)
            res = GetOrderList.GetOrderList(str(sales.value))
            
            res = res[['accountid','customerid','modelinstance','price','quantity','is_buy','exec_type','status']]
            res.set_index('modelinstance',inplace=True)
            
            order_id_lst = list(res[res['status'].isin([1,3,5,6,14])].index)
            
            
            res_disp = pd.DataFrame()
            
            #print(order_id_lst)
            
            res2 = pd.DataFrame()
            
            for each in order_id_lst:
                #print('您全部的订单如下：',str(sales.value),each)
                
                tmp = GetOrderParam.GetOrderParam(str(sales.value),each)

                res2 = res2.append(tmp)
            
            i = 0
            for each in order_id_lst:
                res_disp.loc[i,'订单号'] = each
                res_disp.loc[i,'客户ID'] = int(res.loc[each,'customerid'])
                res_disp.loc[i,'业务员ID'] = int(res.loc[each,'accountid'])
                #res_disp.loc[i,'订单状态'] = res.loc[each,'status'] 
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
                
                res_disp.loc[i,'期权单价'] = res.loc[each,'price']
                res_disp.loc[i,'行权价'] = res2.loc[each,'strike']
                res_disp.loc[i,'期权手数'] = res.loc[each,'quantity']
                res_disp.loc[i,'方向'] = '买入' if res.loc[each,'is_buy']==1 else '卖出'
                if res.loc[each,'status'] == 14:
                    res_disp.loc[i,'状态'] = '下单成功,等待审阅'
                elif res.loc[each,'status'] == 6:
                    res_disp.loc[i,'状态'] = '正在审阅'
                elif res.loc[each,'status'] == 1:
                    res_disp.loc[i,'状态'] = '已通过审阅'
                elif res.loc[each,'status'] == 5:
                    res_disp.loc[i,'状态'] = '未通过审阅'
                elif res.loc[each,'status'] == 3:
                    res_disp.loc[i,'状态'] = '已撤单'
                else:
                    pass
                    
                i+=1
            
            res_disp.index+=1
            display(res_disp)
    
    def withdrawl_click(p):
        clear_output()
        display(sales,withdrawl_order_id,select)
        if sales.value=='无':
            print('请选择业务员ID')
        else:
            res = GetOrderList.GetOrderList(str(sales.value))
            res = res[['accountid','customerid','modelinstance','price','quantity','is_buy','exec_type','status']]
            res.set_index('modelinstance',inplace=True)
            order_id_lst = list(res[res['status'] == 14].index)
            
            if withdrawl_order_id.value in order_id_lst:
                a = UpdateOrderStatus.UpdateOrderStatus('status','3',str(sales.value),withdrawl_order_id.value)
                print('撤单成功')
            else:
                print('无法撤单，请确认输入订单号是否有误')
                #将状态改为取消
    
    def init(p):
        display_()
    
    
    btn_init.on_click(init)
    btn_query.on_click(query_click)
    btn_withdrawl.on_click(withdrawl_click)
    
    tips =  widgets.HTML(value="请先选择【业务员ID】，【查询】自己可撤的订单号，再将订单号复制到文本框【撤单号】并单击【撤单】。")
    
    select = widgets.HBox([btn_query,btn_withdrawl,btn_init])
    display(sales,withdrawl_order_id,tips,select)
    
    
    
def display_():
    btn_ovo = widgets.Button(
        description=u'香草期权下单',
        disabled=False,
        button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击进入香草期权下单界面',
        icon='check'
    )
        
        
    btn_oao = widgets.Button(
        description=u'亚式期权下单',
        disabled=False,
        button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击进入亚式期权下单界面',
        icon='check'
    )
    
    btn_query_withdrawl = widgets.Button(
        description=u'订单查询与撤单',
        disabled=False,
        button_style='info', # 'success', 'info', 'warning', 'danger' or ''
        tooltip=u'单击进入订单查询与撤单界面',
        icon='check'
    )
    
    
    btn_ovo.on_click(on_btn_ovo_clicked)
    btn_oao.on_click(on_btn_oao_clicked)
    btn_query_withdrawl.on_click(on_btn_qw_clicked)
    
    clear_output()
    tips =  widgets.HTML(value="<head><b>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp\
                          版本号：1.0.0</b></head></div>")
    
    select = HBox([btn_ovo,btn_oao,btn_query_withdrawl,tips])
    display(select)
    
    

if __name__ == '__main__':
    #执行语句
    display_()
    