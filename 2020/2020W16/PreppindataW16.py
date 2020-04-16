import pandas as pd
import re

xls = pd.ExcelFile("E:/Can't Desktop Prep this-2.xlsx")
temp = []
for sheet in [sh for sh in xls.sheet_names if re.match('.*Sales$',sh)]:
    df = pd.read_excel(xls,sheet)
    df.insert(0,'Store',re.search('^(.*)\s', sheet).group(1).strip())
    temp.append(df)
sales = pd.concat(temp)   
sales = pd.melt(sales, id_vars=['Store', 'Category', 'Scent'], var_name='Col', value_name='Val')
temp = sales['Col'].str.split(' ', n = 1, expand = True) 
sales['Measure'] = temp[0]
sales['Date'] = pd.to_datetime(temp[1], format='%d/%m/%Y').dt.date
sales = sales.pivot_table(index = ['Store', 'Category', 'Scent','Date'],
                          columns='Measure', values='Val', aggfunc='sum').reset_index()

staff = pd.read_excel(xls,'Staff days worked')
staff['Month'] = staff['Month'].dt.date
staff = pd.melt(staff, id_vars='Month', var_name='Store', value_name='Staff days worked').rename(columns={'Month':'Date'})

final = pd.merge(sales,staff,on=['Date','Store'])[['Store', 'Category', 'Scent', 'Date', 'Sales', 'Profit', 'Staff days worked']]
