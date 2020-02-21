import pandas as pd
import re

xls = pd.ExcelFile("E:/PD 2020 Wk 8 Input Not Random.xlsx")

temp = []
for sheet in [sh for sh in xls.sheet_names if re.search('^Week',sh)]:
    df = pd.read_excel(xls,sheet)
    df.insert(0,'Week',int(re.search('(\d+)',sheet).group(1)))
    temp.append(df.rename(columns={'Volume':'Sales Volume','Value':'Sales Value'}))
sales = pd.concat(temp,sort=False)
sales['Type'] = sales['Type'].str.lower()
sales = sales.groupby(['Type','Week'],as_index=False).agg({'Sales Volume':'sum','Sales Value':'sum'})

profit = pd.read_excel(xls,'Budget',skiprows=2,nrows=16,usecols='C:F')
profit['Week'] = profit['Week '].apply(lambda x:int(re.search('(\d+)$',x).group(1)))
profit['Type'] = profit['Type'].str.lower()

budget = pd.read_excel(xls,'Budget',skiprows=21,nrows=4,usecols='C:G')
budget['Type'] = budget['Type'].apply(lambda x:re.search('([a-z]+)',x.lower()).group(1))
budget['Measure'] = budget['Measure'].apply(lambda x:re.sub('Budget\s','',x))
budget = budget.melt(id_vars=['Type','Measure'],value_name='Budget',var_name='Range')
budget['From Week'] = budget['Range'].apply(lambda x:int(re.search('\-(\d+)\s',str(x)).group(1)))
budget['To Week'] = budget['Range'].apply(lambda x:int(re.search('\-(\d+)\-',str(x)).group(1)))
budget = budget.pivot_table(index=['Type','From Week','To Week'], columns='Measure', values='Budget', aggfunc='sum').reset_index()

finalA = pd.merge(sales,budget,how='inner',on='Type').query(
    '`Week`>=`From Week` and `Week`<=`To Week` and (`Sales Volume`<`Volume` or `Sales Value`<`Value`)')
finalA = finalA[['Type', 'Week', 'Sales Volume', 'Sales Value', 'Volume','Value']].copy()

finalB =  pd.merge(sales,profit,how='inner',on=['Type','Week']).query(
    '`Sales Volume`>`Profit Min Sales Volume` and `Sales Value`>`Profit Min Sales Value`')
finalB = finalB[['Type', 'Week', 'Sales Volume', 'Sales Value', 'Profit Min Sales Volume','Profit Min Sales Value']].copy()
