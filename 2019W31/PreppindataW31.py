import pandas as pd
import numpy as np

actlog = pd.read_excel(pd.ExcelFile(r"E:\PD wk 31 input.xlsx"),"Northern Customer Orders")
actlog['Status'] = actlog['Status'].str.title()

order = actlog.pivot_table(index=['Order','Customer','City'],
                                  columns='Status', values='Date', aggfunc=max)
order.reset_index(inplace=True)
order['time to send'] = order.apply(lambda x: (x['Sent']-x['Purchased'])/np.timedelta64(1,'D'), axis=1)
order['time to review'] = order.apply(lambda x: (x['Reviewed']-x['Sent'])/np.timedelta64(1,'D'), axis=1)
order['Meet KPI'] = order['time to send'].apply(lambda x: 1 if x<=3 else 0)

ans1 = order.groupby(['Customer'], as_index=False).agg({'time to send':'mean'} \
                    ).rename(columns={'time to send':'Avg Time to Send'})
ans2 = order.groupby(['Customer'], as_index=False).agg({'time to review':'mean'} \
                    ).rename(columns={'time to review':'Time to Review from Sending Order'}).dropna()
ans3 = order[pd.isna(order['Sent'])][['City','Purchased','Sent','Order','Customer']]
ans3['Order not sent']='Not Sent'
ans4 = order.groupby(['City'], as_index=False).agg({'Order':'count', 'Meet KPI':'sum'} \
                    ).rename(columns={'Order':'Orders per City','Meet KPI':'Time To Send KPI'})
ans4['% Orders Meeting 3 Day KPI'] = ans4['Time To Send KPI'] / ans4['Orders per City']*100
