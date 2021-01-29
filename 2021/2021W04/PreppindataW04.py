import pandas as pd

xlsx = pd.ExcelFile(r'F:\Data\PD 2021 Wk 4 Input.xlsx')
temp = []
for sheet in [sh for sh in xlsx.sheet_names if sh != 'Targets']:
    df = pd.read_excel(xlsx,sheet)
    df.insert(0,'Store',sheet)
    temp.append(df)
sales = pd.concat(temp) 

sales['Quarter'] = sales['Date'].dt.quarter
sales = sales.drop('Date', axis=1)
sales = pd.melt(sales, id_vars=['Quarter', 'Store'], var_name='Customer Prod', value_name='Products Sold')
sales= sales.groupby(['Quarter', 'Store'], as_index=False).agg({'Products Sold':'sum'})

final = pd.merge(sales,  pd.read_excel(xlsx,'Targets'), on=['Quarter', 'Store'])
final['Variance to Target'] = final['Products Sold'] - final['Target']
final['Rank'] = final.groupby('Quarter')['Variance to Target'].rank(ascending=False).astype(int)
final = final.sort_values(by=['Quarter', 'Rank'])[['Quarter', 'Rank', 'Store', 'Products Sold', 'Target', 'Variance to Target']]
