import pandas as pd
import re
from datetime import timedelta

xls = pd.ExcelFile(r"E:\PD - Week 20.xlsx")
patient = pd.read_excel(xls,"Patient") 
cost_per_visit = pd.read_excel(xls,"Cost per Visit",dtype=str) 
cost_per_visit['To_day'] = cost_per_visit['Length of Stay'].apply(lambda x: int(re.search('\-(\d+)\-',x+'-').group(1)))
cost_per_visit['From_day'] = cost_per_visit['To_day'].shift().fillna(0)

cost_per_day = []
for index, row in cost_per_visit.iterrows():
    cost_per_day = cost_per_day+([int(row['Cost per Day'])] * (row['To_day']-int(row['From_day'])))

cost = pd.DataFrame(cost_per_day,columns=['Cost'])
cost['nday']=cost.index+1
cost['dummy'] = 'dummy'
patient['dummy'] = 'dummy'

data= pd.merge(patient,cost,on='dummy')
data=data[data['nday']<=data['Length of Stay']]
data['Date']=data.apply(lambda x:(x['First Visit']+timedelta(days=x['nday']-1)).date(), axis=1)
data=data[['Name','Date','Cost']].copy()

finalA=data.groupby('Name',as_index=False).agg({'Cost':[('Cost', 'sum'), ('Avg Cost per day per person', 'mean')]})
finalA.columns = [col[1] if col[1] else col[0] for col in finalA.columns.values]

finalB=data.groupby('Date',as_index=False).agg({'Cost':[('Cost per Day', 'sum'), ('Avg Cost per day', 'mean')],
                                                'Name':[('Number of patients','count')]})
finalB.columns = [col[1] if col[1] else col[0] for col in finalB.columns.values]
 
