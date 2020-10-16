import pandas as pd
import re
import datetime 
from datetime import datetime as dt,timedelta

today = datetime.date(2020, 10, 9)
period = pd.DataFrame({'Category':['This Year','Last Year'], 
                       'End Date':[today, dt.strptime(str(int(dt.strftime(today, "%Y"))-1)+dt.strftime(today, "-%U-%w"), "%Y-%U-%w").date()]})
period['WTD']  = period['End Date'].apply(lambda x: x-timedelta(days=int(dt.strftime(x, "%w"))))
period['MTD']  = period['End Date'].apply(lambda x: x.replace(day=1))
period['YTD']  = period['End Date'].apply(lambda x: x.replace(day=1,month=1))
period = period.melt(id_vars = ['Category', 'End Date'], value_name = 'Start Date', var_name='Time Period')
period['Year'] = period['End Date'].apply(lambda x: int(dt.strftime(x, "%Y")))

txn = pd.read_excel(pd.ExcelFile("F:/Data/Transactions.xlsx"),sheet_names=1)  
target = pd.read_excel(pd.ExcelFile("F:/Data/Targets.xlsx"),sheet_names=1)

txn['From Date'] = txn['TransactionDate'].dt.date 
txn['To Date'] = txn['TransactionDate'].dt.date 
txn = txn[txn['TransactionDate'].dt.date>=period['Start Date'].min()][['From Date', 'To Date', 'ProductName', 'Quantity', 'Income']].copy()
txn['Year'] = txn['To Date'].apply(lambda x: int(dt.strftime(x, "%Y")))

target = target.rename(columns={'Quantity Target':'Quantity','Income Target':'Income'})
target['From Date'] = target.apply(lambda x: dt.strptime(f"{x['Year']}-{x['Week']-1}-0",'%Y-%U-%w').date(), axis=1)
target['To Date'] = target['From Date'].apply(lambda x: x+timedelta(days=6))
target = target[['Year', 'From Date', 'To Date', 'ProductName', 'Quantity', 'Income']].copy()
target['Source'] = 'Target'

final = pd.concat([txn, target], sort=False, ignore_index=True)
final = final.merge(period, on='Year', how='inner')
final['Category'] = final.apply(lambda x: x['Category'] if pd.isnull(x['Source']) else x['Source'], axis=1)
final = final[((final['From Date']>=final['Start Date']) & (final['To Date']<=final['End Date']))
              | ((final['From Date']<=final['End Date']) & (final['To Date']>=final['Start Date']))].copy()

final = final.groupby(['ProductName','Category', 'Time Period', 'Metric'], as_index=False).agg({'Who':'count'})

final.columns

output2 = data[~(data['Category']=='Intro')].copy()
output2 = output2.groupby(['Location','Category'], as_index=False).agg({'Who':'count'})
output2 = output2.rename(columns={'Category':'Question or Answer','Who':'Instances'})
