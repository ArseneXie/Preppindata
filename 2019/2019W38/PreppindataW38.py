import pandas as pd

visit = pd.read_csv("E:\Input Data.csv")
visit['Date of Servce'] = visit['Date of Servce'].apply(lambda x: pd.to_datetime(x).date())
visit['Patient Visit Number'] = visit.sort_values('Date of Servce').groupby('PatientID').cumcount()+1
visit['First Visit Date'] = visit['Date of Servce'].groupby(visit['PatientID']).transform('min')
visit['Total Patient Visits'] = visit['Patient Visit Number'].groupby(visit['PatientID']).transform('max')
visit['New Patient Flag'] =visit['Patient Visit Number'].apply(lambda x: 'New Patient' if x==1 else 'Returning Patient')

#check = visit[visit['PatientID']==94]
