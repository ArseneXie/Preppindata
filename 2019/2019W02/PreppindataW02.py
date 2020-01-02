import pandas as pd
import re

xls = pd.ExcelFile("E:\Week Two Input.xlsx")
df = pd.read_excel(xls,xls.sheet_names[0]).dropna()
df= df.query("`City`!='City'").copy()
df['City'] = df['City'].apply(lambda x: 'Edinburgh' if re.match(r'.*gh$',x) else 'London')
df['Value'] = df['Value'].astype('int')
df['Date'] = df['Date'].dt.date
df['R2C Header'] = df['Metric']+' - '+df['Measure']

final = df.drop(['Metric','Measure'],axis=1).pivot_table(index = ['City','Date'],
                                                         columns='R2C Header',
                                                         values='Value',
                                                         aggfunc={'Value':'max'})
final.reset_index(drop=False, inplace=True)
