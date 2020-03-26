import pandas as pd
import re
from datetime import datetime

xls = pd.ExcelFile("E:/PD week 12 input.xlsx")
total_sales = pd.read_excel(xls,'Total Sales').astype({'Year Week Number':str})
percentage = pd.read_excel(xls,'Percentage of Sales')
lookup = pd.read_excel(xls,'Lookup Table')

total_sales['ScentKey'] = total_sales['Scent'].apply(lambda x: re.sub('[^a-z]','',x.lower()))  
total_sales.drop('Scent',axis=1, inplace=True)
percentage['Product'] = percentage['Product ID']+percentage['Size']
percentage['Year Week Number'] = percentage['Week Commencing'].apply(lambda x: datetime.strftime(x,'%Y')+str(int(datetime.strftime(x,'%U'))+1).zfill(2))
percentage = percentage.query('`Percentage of Sales`>0')
lookup['ScentKey'] = lookup['Scent'].apply(lambda x: re.sub('[^a-z]','',x.lower()))  

final = pd.merge(percentage,lookup, on='Product', how='inner')
final = pd.merge(final,total_sales, on=['ScentKey','Year Week Number'], how='inner')
final['Sales'] = final['Total Scent Sales']*final['Percentage of Sales']
final = final[['Year Week Number', 'Scent', 'Size', 'Product Type', 'Sales']].copy()
