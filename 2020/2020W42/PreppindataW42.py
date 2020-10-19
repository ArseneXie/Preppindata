import pandas as pd
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
final['Modifier'] = final.apply(lambda x: (min(x['End Date'],x['To Date'])-max(x['Start Date'],x['From Date'])).days+1, axis=1)
final = final[['ProductName', 'Category', 'Time Period', 'Modifier', 'Quantity', 'Income']].copy()
final = final.melt(id_vars = ['ProductName', 'Category', 'Time Period', 'Modifier'], value_name = 'Value', var_name='Metric')
final['Value'] = final.apply(lambda x: x['Value']/7*x['Modifier'] if x['Category']=='Target' else x['Value'], axis=1)
final = final.groupby(['ProductName','Category', 'Time Period', 'Metric'], as_index=False).agg({'Value':'sum'})
final['Value'] = final['Value'].apply(lambda x: round(x))
final = final.pivot_table(index=['ProductName', 'Metric', 'Time Period'], columns='Category', values='Value', aggfunc=sum).reset_index()
final['% Differece to Last Year'] = round((final['This Year']-final['Last Year'])/final['Last Year'],2)
final['% Differece to Target'] = round((final['This Year']-final['Target'])/final['Target'],2)
final = final[['ProductName', 'Metric', 'Time Period', 'This Year', 'Last Year', 'Target', '% Differece to Last Year', '% Differece to Target']]
