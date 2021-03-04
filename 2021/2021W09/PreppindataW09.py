import pandas as pd
import re
import decimal

context = decimal.getcontext()
context.rounding = decimal.ROUND_HALF_UP

cust_info = pd.read_excel(pd.ExcelFile("F:/Data/Customer Information.xlsx"),sheet_name=0)
cust_info = pd.DataFrame([map(str.strip, x) for x in cust_info['IDs'].str.split(' ').values.tolist()])
cust_info = cust_info.melt(value_name='ID', var_name='ToDrop').drop('ToDrop', axis=1).dropna()
cust_info['Phone'] = cust_info['ID'].apply(lambda x: re.search('(\d{6})(?=,)',x).group(1)) 
cust_info['Area Code Key'] = cust_info['ID'].apply(lambda x: re.search('(?<=,)(\d{2}[A-Z])',x).group(1)) 
cust_info['Product ID'] = cust_info['ID'].apply(lambda x: re.search('([A-Z]+)$',x).group(1)) 
cust_info['Quantity'] = cust_info['ID'].apply(lambda x: int(re.search('(\d+)(?=-)',x).group(1))) 

area_code = pd.read_excel(pd.ExcelFile("F:/Data/Area Code Lookup.xlsx"),sheet_name=0,dtype=str)
area_code = area_code[~area_code['Area'].isin(['Clevedon', 'Fakenham', 'Stornoway'])]
area_code['Area Code Key'] = area_code.apply(lambda x: x['Code'][-2:]+x['Area'][0:1], axis=1)
area_code['Key Count'] = area_code['Area'].groupby(area_code['Area Code Key']).transform('count')

df = pd.merge(cust_info[cust_info['Quantity']>0], area_code[area_code['Key Count']==1], on='Area Code Key')

prod = pd.read_excel(pd.ExcelFile("F:/Data/Product Lookup.xlsx"),sheet_name=0)
prod['Price'] = prod['Price'].apply(lambda x: float(x[1:]))

final = pd.merge(df, prod, on='Product ID')
final['Revenue'] = final['Price']*final['Quantity']
final = final.groupby(['Area', 'Product Name'], as_index=False).agg({'Revenue':'sum'})
final['Revenue'] =final['Revenue'].apply(lambda x: int(round(decimal.Decimal(x), 0)))
final['Area Total'] = final['Revenue'].groupby(final['Area']).transform('sum')
final['Rank'] = final['Revenue'].groupby(final['Area']).rank(ascending=False).astype(int)
final['% of Total – Product'] = final.apply(lambda x: float(round(decimal.Decimal(x['Revenue']/x['Area Total']*100), 2)), axis=1)
final = final[['Rank', 'Area', 'Product Name', 'Revenue', '% of Total – Product']].copy()
