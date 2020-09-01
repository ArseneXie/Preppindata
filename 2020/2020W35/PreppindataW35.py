import pandas as pd

xlsx = pd.ExcelFile("F:/Data/Input Week 35.xlsx")
sales = pd.read_excel(xlsx,'No RowID')   

sales['Store'] = sales['Store'].ffill()
sales = sales.dropna(subset=['Store',sales.columns[1]])
sales['RowID'] = sales.index
sales['MaxRowID'] = sales['RowID'].groupby(sales['Store']).transform('max')
sales['Type'] = sales.apply(lambda x: 'Difference' if x['RowID'] == x['MaxRowID'] 
                            else 'Target' if x['RowID'] == x['MaxRowID']-1 else 'Sales', axis=1)
sales = sales.drop(['RowID','MaxRowID'], axis=1)
sales = sales.melt(id_vars=['Store','Type'], value_name='Value', var_name='Month')
sales['Month'] = sales['Month'].apply(lambda x: pd.to_datetime(x[0:3]+' 01 2020', format='%b %d %Y').date()) 

sales = sales.pivot_table(index=['Store','Month'],columns='Type', values='Value', aggfunc=max).reset_index()
sales = sales[['Store', 'Month', 'Sales', 'Target', 'Difference']]
