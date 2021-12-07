import pandas as pd
import re

xlsx = pd.ExcelFile(r"C:\Data\PreppinData\PD 2021 Wk 48 Input.xlsx")
df = pd.read_excel(xlsx)
df.columns = ['Branch', 'Measure', df[df.columns[2]][0], df[df.columns[3]][0]]

df['Branch'] = df.apply(lambda x: x['Measure'] if isinstance(x[df.columns[2]], str) else None, axis=1)
df['Branch'] = df['Branch'].fillna(method='ffill')
df = df[df['Branch'] != df['Measure']].dropna()

final = df.melt(id_vars=['Branch', 'Measure'], value_name='Value', var_name='Recorded Year')
final['Recorded Year'] = final['Recorded Year'].apply(lambda x: x[-4:]) 
final['Clean Measure Names'] = final['Measure'].apply(lambda x: re.sub('(\s\(.\))$','',x)) 
final['Factor'] = final['Measure'].apply(lambda x: re.search('\((.)\)$',x).group(1) if re.match('.*\(.\)$',x) else '')  
final['True Values'] = final.apply(lambda x: x['Value']*(1000000 if x['Factor']=='m' else 1000 if x['Factor']=='k' else 1), axis=1)
final = final[['Branch', 'Clean Measure Names', 'Recorded Year', 'True Values']]
