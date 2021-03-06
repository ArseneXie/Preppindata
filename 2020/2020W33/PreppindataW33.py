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
final['Week Start'] = final['Date'].apply(lambda x: get_weekstart(x,WED)) 
final = final.groupby(['Week Start','Scent'], as_index=False).agg({'Daily Sales':'sum', 'Units Sold':'sum', 'Cost':'max'})
final = final.merge(order, how='left', left_on='Week Start', right_on='Date').fillna(0)
final['Total Profit'] = final['Daily Sales'] - (final['Units Ordered'] - final['Units Sold'])*final['Cost']

final = final.groupby(['Scent'], as_index=False).agg({'Total Profit':'sum'})
final['Profitability Rank'] = final['Total Profit'].rank(ascending=False)
final = final[['Profitability Rank', 'Scent', 'Total Profit']]
