import pandas as pd

xlsx = pd.ExcelFile(r'F:\Data\PD 2021 Wk 3 Input.xlsx')
temp = []
for sheet in [sh for sh in xlsx.sheet_names]:
    df = pd.read_excel(xlsx,sheet)
    df.insert(0,'Store',sheet)
    temp.append(df)
df = pd.concat(temp) 

df = pd.melt(df, id_vars=['Date', 'Store'], var_name='VAR', value_name='Products Sold')
temp = df['VAR'].str.split('\s-\s', n = 1, expand = True) 
df['Customer Types'] = temp[0] 
df['Product'] = temp[1]
df['Quarter'] = df['Date'].dt.quarter

finalA = df.groupby(['Product','Quarter'], as_index=False).agg({'Products Sold':'sum'})
finalB = df.groupby(['Store','Customer Types','Product'], as_index=False).agg({'Products Sold':'sum'})
