import pandas as pd
import re
from datetime import datetime

xls = pd.ExcelFile(r"E:\PD Wk33.xlsx")

temp = []
for sheet in [sh for sh in xls.sheet_names if re.match('.*Store$',sh)]:
    df = pd.read_excel(xls,sheet)
    df.insert(0,'Store',sheet)
    temp.append(df)
emp_sal = pd.concat(temp)   
emp_sal['End Date'].fillna(datetime(2019,10,1,0,0),inplace=True)
emp_sal = emp_sal[emp_sal['End Date']>=datetime(2019,1,1,0,0)]
emp_sal['Start Date'] = emp_sal['Start Date'].dt.date
emp_sal['End Date'] = emp_sal['End Date'].dt.date

sal_range = pd.read_excel(xls,'Salary Range')
temp = sal_range['Range'].str.split('-',n = 1, expand = True)
sal_range['Salary Range Minimum'] = temp[0].apply(lambda x: int(re.sub('[^\d]','',x)))
sal_range['Salary Range Maximum'] = temp[1].apply(lambda x: int(re.sub('[^\d]','',x)))
sal_range['Bonus amount'] = sal_range['Bonus amount'].apply(lambda x: int(re.sub('[^\d]','',x)))
sal_range['Salary Rank'] = sal_range['Salary Range Maximum'].rank(ascending=False)
sal_range['Assumed Position Based on Salary Range'] = sal_range['Salary Rank'].apply(
        lambda x: 'Area Manager' if x == 1 else ('Manager' if x == 2 else 'Team Member'))

emp_sal['dummy']='d' 
sal_range['dummy']='d'
emp_bns = pd.merge(emp_sal,sal_range,on='dummy')
emp_bns_within = emp_bns.query('Salary>=`Salary Range Minimum` and Salary<=`Salary Range Maximum`')
emp_bns_without = emp_sal[~emp_sal['Name'].isin(emp_bns_within['Name'])]
emp_bns = pd.concat([emp_bns_within,emp_bns_without],axis=0, ignore_index=True, sort=False)

final1 = emp_bns.drop(['dummy','Salary Rank'], axis=1).copy()
final1['Correct Salay for Role'] = final1.apply(lambda x: x['Role']==x['Assumed Position Based on Salary Range'],axis=1)
final1['Pay Stuts'] = final1.apply(lambda x: 'Incorrect Pay' if pd.isnull(x['Range']) else 'Assumed Coreect Pay',axis=1)
final1 = final1[~final1['Correct Salay for Role']]


sales = pd.read_excel(xls,'Store Sales')
sales = sales.melt(id_vars=['Store', 'Quarterly Target'], value_name='MonSales', var_name='Sales Date')
sales['QCheckDate'] = sales['Sales Date'].apply(lambda x: (x+pd.offsets.QuarterEnd()-pd.offsets.MonthBegin(n=1)).date())
qsales = sales.groupby(['Store','QCheckDate'],as_index=False).agg({'MonSales':'sum', 'Quarterly Target':'max'})
qsales = qsales[qsales['MonSales']>=qsales['Quarterly Target']][['Store','QCheckDate']]
qsales['Store'] = qsales['Store']+' Store'

final2 = pd.merge(emp_bns,qsales,on='Store')
final2 = final2.query('`Start Date`<=`QCheckDate` and `End Date`>=`QCheckDate`')
final2 = final2.groupby(['Store','Name','Salary'],as_index=False).agg({'Bonus amount':'sum'})
final2['% Bonus of Salary'] = final2['Bonus amount']/final2['Salary']*100
