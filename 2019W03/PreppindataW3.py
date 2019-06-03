import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta

xls = pd.ExcelFile("H:\PreppinData - Week Three.xlsx")

df = pd.read_excel(xls,"Contract Details") 

final = df.iloc[np.repeat(np.arange(len(df)), list(df['Contract Length (months)']))].copy()
final['rownum'] = final.groupby(['Name'])['Start Date'].rank(method='first')
final['Payment Date'] = final.apply(lambda x: pd.to_datetime(x['Start Date']) \
     + relativedelta(months=x['rownum']-1),axis=1) 
final = final[['Payment Date','Name','Monthly Cost','Contract Length (months)','Start Date']]