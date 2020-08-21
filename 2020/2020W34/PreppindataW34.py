import pandas as pd
from datetime import timedelta

MON, TUE, WED, THU, FRI, SAT, SUN = range(7)

def get_weekstart(xdate, startwd):
    offset = (xdate.weekday()-startwd)%7
    return xdate - timedelta(days=offset)

xlsx = pd.ExcelFile("F:/Data/2020W33.xlsx")
order = pd.read_excel(xlsx,'Orders')   
prod= pd.read_excel(xlsx,'Scent')   
sales = pd.read_excel(xlsx,'Daily Sales')  

final = pd.merge(sales,prod, on='Scent Code')
final['Units Sold'] = final['Daily Sales']/final['Price'] 
w34 = final.copy()   #<-- additional for W34
final['Week Start'] = final['Date'].apply(lambda x: get_weekstart(x,WED)) 
final = final.groupby(['Week Start','Scent'], as_index=False).agg({'Daily Sales':'sum', 'Units Sold':'sum', 'Cost':'max'})
temp = final         #<-- additional for W34
final = final.merge(order, how='left', left_on='Week Start', right_on='Date').fillna(0)
final['Total Profit'] = final['Daily Sales'] - (final['Units Ordered'] - final['Units Sold'])*final['Cost']

final = final.groupby(['Scent'], as_index=False).agg({'Total Profit':'sum'})
final['Profitability Rank'] = final['Total Profit'].rank(ascending=False)
final = final[['Profitability Rank', 'Scent', 'Total Profit']]

#-- additional process for W34
from math import ceil

w33 = final[['Scent', 'Total Profit']]
w34 = w34.groupby('Scent', as_index=False).agg({'Units Sold':'mean', 'Price':'max'})
w34['Plan Ordered'] = w34['Units Sold'].apply(lambda x: round(ceil(x),-1)*7)
w34 = pd.merge(w34.drop('Units Sold', axis=1), temp, on='Scent')
w34['Units Sold'] = w34.apply(lambda x: min(x['Units Sold'], x['Plan Ordered']), axis=1)
w34['Waste'] = w34['Plan Ordered'] - w34['Units Sold']
w34['New Profit'] = w34['Units Sold']*w34['Price'] - w34['Waste']*w34['Cost'] 
w34 = w34.groupby(['Scent'], as_index=False).agg({'New Profit':'sum'})

final = pd.merge(w33, w34, on='Scent')
final['Difference'] = final['New Profit'] - final['Total Profit'] 
