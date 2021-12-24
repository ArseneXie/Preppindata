import pandas as pd

xlsx = pd.ExcelFile(r"C:\Data\PreppinData\Sales Department Input.xlsx")

temp = []
for sheet in xlsx.sheet_names:
    df = pd.read_excel(xlsx,sheet)
    df.insert(0,'Month',sheet)
    temp.append(df)
sales = pd.concat(temp)

sales = sales.rename(columns={sales.columns[-1]:'Oct YTD Total'})
sales[['Salesperson','Oct YTD Total']] = sales[['Salesperson','Oct YTD Total']].fillna(method='bfill') 
sales = sales[pd.notna(sales['Date'])]

sales['Oct YTD Total'] = sales['Oct YTD Total'].groupby(sales['Salesperson']).transform('max')
sales['Monthly Total'] = sales['Total'].groupby([sales['Month'], sales['Salesperson']]).transform('sum')
sales['YTD Total'] = sales.apply(lambda x: x['Oct YTD Total'] + (x['Monthly Total'] if x['Month']=='November' else 0), axis=1)

sales = sales[['Date', 'Salesperson', 'Road', 'Gravel', 'Mountain', 'YTD Total']].copy()
sales = sales.melt(id_vars=['Salesperson', 'Date', 'YTD Total'], value_name='Sales', var_name='Bike Type')
sales = sales[['Salesperson', 'Date', 'Bike Type', 'Sales', 'YTD Total']]
