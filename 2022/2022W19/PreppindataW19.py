import pandas as pd

xlsx = pd.ExcelFile(r"C:\Data\PreppinData\PD 2022 Wk 19 Input.xlsx")

prodset = pd.read_excel(xlsx, 'Product Set').rename(columns={'Size':'Product Size'})
prodset['Product Code'] = prodset['Product Code'].str.replace('S','')

sales = pd.read_excel(xlsx, 'Sales')
size = pd.read_excel(xlsx, 'Size Table').rename(columns={'Size':'Sales Size'})

sales = sales.merge(size, left_on='Size', right_on='Size ID')
sales = sales.merge(prodset, left_on='Product', right_on='Product Code')

correct_sales = sales.query('`Sales Size`==`Product Size`')[['Product Size', 'Scent', 'Product', 'Store']]

wrong_sales = sales.query('`Sales Size`!=`Product Size`')[['Product Size', 'Scent', 'Product Code', 'Store']]
wrong_sales = wrong_sales.groupby(['Product Code', 'Product Size', 'Scent'], as_index=False).agg({'Store':'count'})
wrong_sales = wrong_sales.rename(columns={'Store':'Number of Sales with wrong size'})
