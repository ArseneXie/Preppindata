import pandas as pd
import re

sch = pd.read_excel(r'E:\PD - Week 34.xlsx','Delivery Schedule')
sch['nth'] = sch['Delivery Schedule'].apply(lambda x: int(re.search(r'^(\d+)',x).group(1)))
sch['Weekday'] = sch['Delivery Schedule'].apply(lambda x: re.search(r'.*\s(.*)\sof',x).group(1))

date = pd.read_excel(r'E:\PD - Week 34.xlsx','Date Scaffold')
date['Date'] = date['Date'].apply(lambda x: x.date())
date['YearMonth'] = date['Date'].apply(lambda x: x.strftime('%Y%m'))
date['Weekday'] = date['Date'].apply(lambda x: x.strftime('%A'))
date['Month Name'] = date['Date'].apply(lambda x: x.strftime('%B'))
date['nth'] = date.sort_values('Date').groupby(['YearMonth','Weekday']).cumcount()+1
date=date[['Date','Weekday','nth','Month Name']].copy()

final = pd.merge(sch,date,on=['Weekday','nth'],how='inner')
final=final[['Month Name','Weekday','Date','Product','Scent','Supplier','Quantity']].sort_values(by=['Date']).copy().reset_index(drop=True)
