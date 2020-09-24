import pandas as pd
import re

order = pd.read_excel(pd.ExcelFile("F:/Data/2020W39 Input.xlsx"),'Orders')  
order = order.melt(id_vars='Person', value_name = 'Order Item', var_name='Weekday').dropna()
order = pd.concat([order[['Person','Weekday']].reset_index(drop=True), 
                   pd.DataFrame([map(str.strip, x) for x in order['Order Item'].str.split(',|with').values.tolist()])],
                  axis=1, sort=False)
order =  order.melt(id_vars=['Person','Weekday'], value_name = 'Order Item', var_name='ToDrop').dropna()
order['Order Item'] = order['Order Item'].apply(lambda x: re.sub('\s*(tea|(fruit )*smoothie)$','',x.lower()))

price = pd.read_excel(pd.ExcelFile("F:/Data/2020W39 Input.xlsx"),'Price List')  
price = price.melt(id_vars = [c for c in price.columns if re.search('Price$',c)], value_name = 'Item', var_name='Type').dropna(subset=['Item'])
price = price.melt(id_vars = ['Type','Item'], value_name = 'Price', var_name='Price Type').dropna()
price = price[price['Type'] +' Price' == price['Price Type']].copy()
price['Item'] = price['Item'].apply(lambda x: re.sub('\s*(tea|(fruit )*smoothie)$','',x.lower()))

final = pd.merge(order,price,left_on='Order Item', right_on='Item')
final = final.groupby('Person', as_index=False).agg({'Price':'sum'})
final['Monthly Spend'] = final['Price']*4
final['Potential Savings'] = final['Monthly Spend']-20
final['Worthwhile?'] = final['Potential Savings'].apply(lambda x: x>=0)
final = final.drop('Price', axis=1)
