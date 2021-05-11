import pandas as pd
import re

xlsx = pd.ExcelFile("F:/Data/Preppin Data Challenge.xlsx")

df = pd.read_excel(xlsx,sheet_name=0)
df = df.dropna(subset=[df.columns[0]]).drop([t for t in df.columns if re.match('^[Unnamed|Project]',str(t))],axis=1)     
df[df.columns[-1]] = df[df.columns[-1]].apply(lambda x: None if isinstance(x,str) else x)
df = df.melt(id_vars=[df.columns[0]], var_name='Date', value_name='Hours').dropna()
df['Name'] = df[df.columns[0]].apply(lambda x: re.search('(.*),',x).group(1))
df['Area of Work'] = df[df.columns[0]].apply(lambda x: re.search('(?<=:\s)(.*)$',x).group(1))

dk = df.groupby(['Name']).agg({'Date':'nunique', 'Hours':'sum'})
dk['Avg Hours'] = dk['Hours']/dk['Date']
final = df[df['Area of Work']!='Chats'].groupby(['Name', 'Area of Work']).agg({'Hours':'sum'})
final['% of Total'] = final.groupby(level=0).apply(lambda x: round(100 * x / float(x.sum())))
final['% of Total'] = final['% of Total'].apply(lambda x: f'{int(x)}%') 
final = final.reset_index(drop=False).drop('Hours', axis=1)
final = final[final['Area of Work']=='Client']
final['Avg Number of Hours worked per day'] = final['Name'].apply(lambda x: dk.loc[x,'Avg Hours'])
