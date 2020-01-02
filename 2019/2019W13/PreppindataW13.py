import pandas as pd
from datetime import timedelta

xls = pd.ExcelFile("E:\PD - Week 13.xlsx")
trans = pd.read_excel(xls,"Transactions") 
customer = pd.read_excel(xls,"Customer Look-up") 

temp = trans.merge(customer,on='Account', how='inner')
temp['Week']=temp.apply(lambda x: int(x['Date'].strftime("%U"))+1,axis=1)
temp['Week date']=temp.apply(lambda x: max(x['Date'].replace(month=1,day=1),  
    x['Date'] - timedelta(days=(x['Date'].weekday()+1)%7)).strftime("%Y/%m/%d"),axis=1)
temp['Month']=temp.apply(lambda x: x['Date'].month,axis=1)
temp['Month date']=temp.apply(lambda x: x['Date'].replace(day=1).strftime("%Y/%m/%d"),axis=1)
temp['Quarter']=temp.apply(lambda x: (x['Date'].month-1)//3+1,axis=1)
temp['Quarter date']=temp.apply(lambda x: x['Date'].replace(month=x['Quarter']*3-2,day=1).strftime("%Y/%m/%d"),axis=1)
temp['Days Below Zero balance'] = temp.apply(lambda x: 1 if x['Balance']<0 else 0,axis=1)
temp['Days Beyond Max Credit'] = temp.apply(lambda x: 1 if x['Balance']*-1>x['Max Credit'] else 0,axis=1)

agg_col = {'Transaction':'mean',
           'Balance':'mean',
           'Days Below Zero balance':'sum',
           'Days Beyond Max Credit':'sum'}

final = {}
for period in ['Week','Month','Quarter']:
    final[period] = temp.groupby(['Account','Name',period,period+' date'], as_index=False).agg(agg_col)
    final[period].rename(columns=
          {period+' date':'Date','Transaction':period+'ly Avg Transaction','Balance':period+'ly Avg Balance'},
          inplace=True)
