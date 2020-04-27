import pandas as pd
import numpy as np
import re

xls = pd.ExcelFile("E:/PD 2020W17 Shows and Devices.xlsx")
dev_list = pd.read_excel(xls,'Devices')
dev_list['Device_lower'] = dev_list['Device'].str.lower()
show_list = pd.read_excel(xls,'Netflix Shows').drop_duplicates()
show_list['Show'] = show_list['TV Shows/Movies'].apply(lambda x: re.search("([^\(]+)",str(x)).group(1).strip().upper())

survey = pd.read_excel(pd.ExcelFile("E:/PD 2020W17 Survey.xlsx"),sheet_name=0)
survey = survey.drop('Timestamp', axis=1).drop_duplicates()

device = pd.DataFrame([map(str.strip, map(str.lower,x)) for x in survey['How have you been watching Netflix? (Phone, TV, etc.)']
                     .str.split(',|&').values.tolist()])
device = device.melt(value_name='Device_lower', var_name='To_drop').replace({'Device_lower': {'etc.': np.nan}}).drop('To_drop', axis=1).dropna()
device = pd.merge(device, dev_list, on='Device_lower', how='left',indicator='Join')
device['Device'] = device.apply(lambda x:x['Device'] if x['Join']=='both' else 'Other', axis=1)
device = device.groupby('Device', as_index=False).agg({'Join':'count'}).rename(columns={'Join':'Count'})


show_in_Q = [re.search('rate ([^\?]+)(?=\?)',c).group(1).upper() for c in survey.columns if re.search('rate ([\w\s\-]+)(?=\?)',c)]
show = pd.concat([survey[['How would you rate "Other"?']].rename(columns={'How would you rate "Other"?':'Rate'}), 
                  pd.DataFrame([map(str.strip, map(str.upper,x)) for x in survey['What have you been binging during lockdown?']
                                .str.split(',').values.tolist()])], axis=1, sort=False)
show = show.melt(id_vars='Rate', value_name='Show', var_name='To_drop').drop('To_drop', axis=1).dropna()
show = pd.merge(show, show_list, on='Show')
show['Is Other'] = show['Show'].apply(lambda x: str(x) not in show_in_Q)
show = show[show['Is Other']][['Show','Rate']].copy()

showQ = survey[[c for c in survey.columns if re.search('rate ([\w\s\-]+)(?=\?)',c) or re.search('(lockdown)',c)]].rename(
    columns={'What have you been binging during lockdown?':'lockdown'})
showQ = showQ.melt(id_vars='lockdown', value_name='Rate', var_name='Show').dropna()
showQ['Show'] = showQ['Show'].apply(lambda x: re.search('rate ([^\?]+)(?=\?)',x).group(1).upper())
showQ['Is Lockdown'] = showQ.apply(lambda x: True if re.search(f'({x["Show"]})',x['lockdown'],re.I) else False, axis=1)

show = show.append(showQ[showQ['Is Lockdown']][['Show','Rate']].copy())
show = show.groupby('Show', as_index=False).agg({'Rate':'mean'})
show['Rank'] = show['Rate'].rank(method='dense', ascending=False).astype(int)
