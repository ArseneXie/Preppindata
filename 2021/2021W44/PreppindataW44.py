import pandas as pd
import re

process = pd.read_csv("C:\\Data\\PreppinData\\Bike Painting Process - Painting Process.csv")
process['Datetime'] = process.apply(lambda x: pd.to_datetime(f"{x['Date']} {x['Time']}"), axis=1)
process = process.groupby(['Batch No.']).apply(pd.DataFrame.sort_values, 'Datetime', ascending=True).reset_index(drop=True)
 
for attr in ['Bike Type', 'Batch Status', 'Name of Process Stage']:
    process[attr] = process.apply(lambda x: x['Data Value'] if x['Data Parameter']==attr else None, axis=1)
    process[attr] = process.groupby(['Batch No.'])[attr].ffill() 
    
process = process[(process['Data Type']=='Process Data') & (process['Data Parameter']!='Name of Process Stage')]
for vtype in ['Actual', 'Target']:
    process[vtype] = process.apply(lambda x: float(x['Data Value']) if re.match(f'^({vtype})',x['Data Parameter']) else None, axis=1)
process['Data Parameter'] = process['Data Parameter'].apply(lambda x: re.sub('^(\w+\s)','',x))
process = process[['Batch No.', 'Bike Type', 'Batch Status', 'Name of Process Stage',
                   'Data Parameter', 'Actual', 'Target', 'Datetime']]
   

