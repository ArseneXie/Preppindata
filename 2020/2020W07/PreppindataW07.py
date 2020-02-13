import pandas as pd
import re
from datetime import datetime

leaver = pd.read_csv(r'E:/PD 2020 Wk 7 Leavers Input.csv')
employee = pd.read_csv(r'E:/PD 2020 Wk 7 Current Employees Input.csv')
report_date = pd.read_csv(r'E:/PD 2020 Wk 7 Reporting Date Input.csv')

report_date['Month'] = report_date['Month'].apply(lambda x: datetime.strptime(x,'%b-%Y').date())
report_date['key'] = 'dummy'
leaver['Join Date'] = leaver['Join Date'].apply(lambda x: datetime.strptime(x,'%m/%d/%Y').date())
leaver['Leave Date'] = leaver['Leave Date'].apply(lambda x: datetime.strptime(x,'%m/%d/%Y').date())
leaver['key'] = 'dummy'
employee['Join Date'] = employee['Join Date'].apply(lambda x: datetime.strptime(x,'%m/%d/%Y').date())
employee['Salary'] = employee['Salary'].apply(lambda x: int(re.sub('\D','',x)))
employee['key'] = 'dummy'

leaver = pd.merge(leaver,report_date,how='inner',on='key')
leaver['Valid'] = leaver.apply(lambda x: 
                               x['Join Date']<=x['Month']+pd.offsets.MonthEnd(n=1) 
                               and x['Leave Date']>=x['Month']+pd.offsets.DateOffset(months=1),axis=1)
employee = pd.merge(employee,report_date,how='inner',on='key')
employee['Valid'] = employee.apply(lambda x: x['Join Date']<=x['Month']+pd.offsets.MonthEnd(n=1),axis=1)  
final = pd.concat([employee[employee['Valid']][['Month','Employee ID','Salary']],
                   leaver[leaver['Valid']][['Month','Employee ID','Salary']]]).copy()
final = final.groupby('Month',as_index=False).agg({'Employee ID':[('Current Employees','count')],
                                                   'Salary':[('Total Monthly Salary','sum'),
                                                             ('Avg Salary per Current Employees','mean')]})
final.columns = [col[1] if col[1] else col[0] for col in final.columns.values]
