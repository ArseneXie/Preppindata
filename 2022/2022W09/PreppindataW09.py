import pandas as pd
import re

classification = {'N':'New', 'C':'Consistent', 'S':'Sleeping', 'R':'Returning'}

xlsx = pd.ExcelFile(r"C:\Data\PreppinData\Sample - Superstore.xls")

sales = pd.read_excel(xlsx,'Orders')
sales['Year'] = sales['Order Date'].apply(lambda x: x.year)

customer = sales.groupby(['Customer ID', 'Customer Name', 'Year'], as_index=False).agg({'Order ID':'count'})
customer['First Purchase'] = customer['Year'].groupby(customer['Customer ID']).transform('min')
customer = customer.pivot_table(index=['Customer ID', 'Customer Name', 'First Purchase'],
                                columns='Year', values='Order ID', aggfunc=max).reset_index()
customer = customer.melt(id_vars=['Customer ID', 'Customer Name', 'First Purchase'], value_name='Order?', var_name='Year')
customer['Order?'] = customer['Order?'].apply(lambda x: 0 if pd.isnull(x) else 1) 
customer['Position'] = customer['Year'] - customer['Year'].min()
customer['Power'] = customer['Year'].max() - customer['Year']
customer['Temp'] = customer['Order?']*(10**customer['Power']) 
customer['OrderString'] = customer['Temp'].groupby(customer['Customer ID']).transform('sum')
customer['OrderString'] = customer['OrderString'].apply(lambda x: re.sub('0', 'S', re.sub('(?<=0)(1)', 'R', re.sub('(?<!0)(1)', 'C', re.sub('(^1)', 'N', str(x))))).rjust(4, '-'))
customer['Customer Classification'] = customer.apply(lambda x: classification.get(x['OrderString'][x['Position']],'-'), axis=1)
customer = customer[customer['Customer Classification']!='-'][['Customer ID', 'Customer Name', 'First Purchase', 'Year', 'Order?', 'Customer Classification']]

cohort = customer.groupby(['First Purchase', 'Year'], as_index=False).agg({'Order?':'sum'})
cohort = cohort.sort_values(['First Purchase', 'Year'])
cohort['Previous'] = cohort.groupby('First Purchase')['Order?'].transform(lambda x: x.shift(1))
cohort['YoY Difference'] = cohort.apply(lambda x: (x['Order?'] - x['Previous']) if x['Year'] > x['First Purchase'] else None, axis=1 )

customer = pd.merge(customer, cohort[['First Purchase', 'Year', 'YoY Difference']], on=['First Purchase', 'Year'])
final = pd.merge(customer, sales, on=['Customer ID', 'Customer Name', 'Year'], how='left')

