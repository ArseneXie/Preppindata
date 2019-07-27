import pandas as pd
import re
from datetime import datetime as dt,timedelta
import time 

xls = pd.ExcelFile("E:/PD - Week 23.xlsx")

temp = []
for sheet in xls.sheet_names:
    df = pd.read_excel(xls,sheet)
    df.insert(0,'Start Date',re.search('wc\s(.*)', sheet).group(1).strip()+' 2019')
    temp.append(df)
final = pd.concat(temp)   

final['Start Date'] = final['Start Date'].apply(lambda x: dt.strptime(re.sub('(?<=[0-9])(?:st|nd|rd|th)','',x), '%d %b %Y').date())
final['Date'] = final.apply(lambda x: x['Start Date']+timedelta(days=time.strptime(x['Day'], '%A').tm_wday),axis=1)
final['Notes'] = final['Notes'].apply(lambda x: x.title())
final['Name'] = final['Notes'].apply(lambda x: re.search('(.*)\sWant', x).group(1))
final['Value'] = final['Notes'].apply(lambda x: int(re.search('£(\d+)', x).group(1)))
final['Scent'] = final['Notes'].apply(lambda x: re.search('(\w+)\s\w+\s\w+$', x).group(1))
final['Product'] = final['Notes'].apply(lambda x: re.search('(\w+\s\w+$)', x).group(1))

final.drop(['Day','Start Date'],axis=1,inplace = True)
