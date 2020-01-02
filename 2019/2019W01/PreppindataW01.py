import pandas as pd
import re
import datetime

xls = pd.ExcelFile("E:\Week 1 Input.xlsx")
df = pd.read_excel(xls,xls.sheet_names[0])
df.drop([col for col in df.columns if re.match(r'^Unnamed',col)], axis=1, inplace=True) 
df['Date'] = df.apply(lambda x: datetime.date(x['When Sold Year'], x['When Sold Month'], 1),axis=1)
df['Total Cars Sold'] = df['Red Cars']+df['Silver Cars']+df['Black Cars']+df['Blue Cars']
df.drop(['When Sold Year','When Sold Month'], axis=1, inplace=True)