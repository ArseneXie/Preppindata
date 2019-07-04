import pandas as pd
import re
from datetime import timedelta,datetime
from dateutil.relativedelta import relativedelta

xls = pd.ExcelFile(r"E:\PD - Week 20.xlsx")
patient = pd.read_excel(xls,"Patient") 
cost_per_visit = pd.read_excel(xls,"Cost per Visit",dtype=str) 
cost_per_visit['To_day'] = cost_per_visit['Length of Stay'].apply(lambda x: int(re.search('\-(\d+)\-',x+'-').group(1)))
cost_per_visit['From_day'] = cost_per_visit['To_day'].shift().fillna(0)

checkup =  pd.read_excel(xls,"Frequency of Check-ups") 
checkup = checkup.append({'Check-up':'Origin', 'Months After Leaving':0, 'Length of Stay':0}, ignore_index=True)
checkup['dummy'] = 'dummy'

patientcsv = pd.read_csv("E:\PD - Week 21 - Patients.csv")
patientcsv['First Visit'] = patientcsv['First Visit'].apply(lambda x: datetime.strptime(x, "%d/%m/%Y"))
patientcsv.rename(columns={'Patient Name': 'Name'},inplace=True)
patient = pd.concat([patient, patientcsv])
patient.rename(columns={'Length of Stay': 'Origin Stay'},inplace=True)
patient['dummy'] = 'dummy'

patient = pd.merge(patient,checkup,on='dummy')

patient['Length of Stay'] = patient.apply(lambda x: x['Origin Stay'] if x['Check-up']=='Origin' else x['Length of Stay'] , axis=1)
patient['First Visit'] = patient.apply(lambda x: \
     x['First Visit'] if x['Check-up']=='Origin' else \
     x['First Visit'] +relativedelta(days=x['Origin Stay']-1,months=x['Months After Leaving']), axis=1)

cost_per_day = []
for index, row in cost_per_visit.iterrows():
    cost_per_day = cost_per_day+([int(row['Cost per Day'])] * (row['To_day']-int(row['From_day'])))

cost = pd.DataFrame(cost_per_day,columns=['Cost'])
cost['nday']=cost.index+1
cost['dummy'] = 'dummy'

data= pd.merge(patient,cost,on='dummy')
data=data[data['nday']<=data['Length of Stay']]
data['Date']=data.apply(lambda x:(x['First Visit']+timedelta(days=x['nday']-1)).date(), axis=1)
data=data[['Name','Date','Cost']].copy()

finalA=data.groupby('Name',as_index=False).agg({'Cost':[('Cost', 'sum'), ('Avg Cost per day per person', 'mean')]})
finalA.columns = [col[1] if col[1] else col[0] for col in finalA.columns.values]

finalB=data.groupby('Date',as_index=False).agg({'Cost':[('Cost per Day', 'sum'), ('Avg Cost per day', 'mean')],
                                                'Name':[('Number of patients','count')]})
finalB.columns = [col[1] if col[1] else col[0] for col in finalB.columns.values]
 
