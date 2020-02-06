import pandas as pd
import re

xlsx = pd.ExcelFile(r'E:/PD 2020 Wk 6 Input.xlsx')
conv = pd.read_excel(xlsx, 'GBP to USD conversion rate')
conv['Week'] = conv['Date'].apply(lambda x: 'wk '+str(int(x.strftime('%U'))+1)+x.strftime(' %Y'))
conv['Conv Rate'] = conv['British Pound to US Dollar'].apply(lambda x: float(re.search('(?<=\s)(\d\.\d+)',x).group(1)))
conv = conv.groupby('Week',as_index=False).agg({'Conv Rate':[('Max Conv Rate','max'),('Min Conv Rate','min')]})
conv.columns = [col[1] if col[1] else col[0] for col in conv.columns.values]

sales = pd.read_excel(xlsx, 'Sales')
sales['Week'] = sales.apply(lambda x: 'wk '+str(x['Week'])+' '+str(x['Year']), axis=1)
sales['UK Sales Value (GBP)'] = sales['Sales Value']*(1-sales['US Stock sold (%)']/100)
sales['US Sales Value (GBP)'] = sales['Sales Value']-sales['UK Sales Value (GBP)']

final = pd.merge(sales,conv,how='inner',on='Week')
final['US Sales (USD) Best Case'] = final['US Sales Value (GBP)']*final['Max Conv Rate']
final['US Sales (USD) Worst Case'] = final['US Sales Value (GBP)']*final['Min Conv Rate']
final['US Sales Potential Variance'] = final['US Sales (USD) Best Case']-final['US Sales (USD) Worst Case']
final = final[['Week', 'UK Sales Value (GBP)', 'US Sales (USD) Best Case', 'US Sales (USD) Worst Case', 'US Sales Potential Variance']].copy()
