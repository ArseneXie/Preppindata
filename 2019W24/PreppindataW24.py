import pandas as pd
import re
from datetime import datetime as dt

calendar = pd.read_excel(pd.ExcelFile(r"E:\Dates Input.xlsx"),"Dates") 
calendar['Date']=calendar['Date'].apply(lambda x: dt.strptime(x+' 2019','%d %B %Y').date())

chat = pd.read_excel(pd.ExcelFile(r"E:\Messages Input.xlsx"),"chat")
chat['Name']=chat['Field_1'].apply(lambda x: re.search(']\s+\W*((\w+\s*)+)\W', x).group(1))
chat['Message']=chat['Field_1'].apply(lambda x: re.search(':\s+\W*(.*)', x).group(1))
chat['Number of Words']=chat['Message'].apply(lambda x:  len(x.split()))
chat['Date']=chat['Field_1'].apply(lambda x: dt.strptime(re.search('(\d+/\d+/\d+)', x).group(1),'%d/%m/%Y').date())
chat['Hour']=chat['Field_1'].apply(lambda x: int(re.search('\s(\d+):', x).group(1)))

chatdata = pd.merge(chat, calendar, how='inner', on='Date')
chatdata['Send from work']=chatdata.apply(lambda x: 1 if x['Holiday?']=='Weekday' and (9<=x['Hour']<12 or 13<x['Hour']<17) else 0,axis=1)
final = chatdata.groupby('Name',as_index=False).agg({'Number of Words':[('Number of Words', 'sum'), ('Avg Words/Sentence', 'mean')],
                     'Send from work':[('Text While at Work', 'sum'), ('% Send from Work', 'mean')],
                     'Message':[('Text','count')]})
final.columns = [col[1] if col[1] else col[0] for col in final.columns.values]
final['% Send from Work']=final['% Send from Work']*100
