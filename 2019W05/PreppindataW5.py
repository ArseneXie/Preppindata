import pandas as pd
import re
from datetime import datetime as dt,timedelta
import time 

xls = pd.ExcelFile("E:/week5input.xlsx")

temp = []
for sheet in xls.sheet_names:
    df = pd.read_excel(xls,sheet)
    df.insert(0,'Start Date',re.search('.*commencing (.*)', sheet).group(1).strip())
    temp.append(df)
final = pd.concat(temp)   

final['Start Date'] = final.apply(lambda x: dt.strptime(re.sub('(?<=[0-9])(?:st|nd|rd|th)','',x['Start Date']), '%d %B %y'),axis=1)
final['Ture Date'] = final.apply(lambda x: x['Start Date']+timedelta(days=time.strptime(x['Date'], '%A').tm_wday),axis=1)

for check in [['Statement?','statement'],['Balance?','balance'],['Complaint','complain']]:
    final[check[0]] = final.apply(lambda x: 1 if bool(re.search(check[1], x['Notes'], re.IGNORECASE)) else 0 ,axis=1)
    
final['Policy Number'] = final.apply(lambda x: re.search('.*#([0-9]+).*',x['Notes']).group(1).strip() \
     if bool(re.search('#[0-9]+', x['Notes'], re.IGNORECASE)) else None ,axis=1)    
final.dropna(inplace=True)
final.drop(['Date','Start Date','Notes'],axis=1,inplace = True)
final.reset_index(drop=True,inplace=True)