import pandas as pd
import re

xls = pd.ExcelFile("E:/PD - Wk 43 - Next Year's Store Targets-2.xlsx")
sales = pd.read_excel(xls,'Monthly Sales Value')
target = pd.read_excel(xls,'Quarterly Store Targets')
action = pd.read_excel(xls,'Targets - Next steps')

sales = sales[sales['Store']!='Total'].copy()
sales = sales.melt(id_vars='Store', value_name='Sales', var_name='Month')
sales['Quarter'] = sales['Month'].apply(lambda x: (int(re.search(r'\s(\d+)\s',x).group(1))-1)//3+1)
sales = sales.groupby(['Store','Quarter'], as_index=False).agg({'Sales':'sum'})

target = target.melt(id_vars=['Location','Region'], value_name='Target Value', var_name='Quarter')
target['Quarter'] = target['Quarter'].apply(lambda x: int(re.search('(\d+)',x).group(1)))

final = pd.merge(sales,target,how='inner', left_on=['Store','Quarter'], right_on = ['Location','Quarter'])
final['Variance to Target'] = final['Sales'] - final['Target Value'] 
final['Variance to Target X'] = round(final['Sales']/final['Target Value']*100)

action.rename(columns = {action.columns[2]:'Actions'}, inplace=True)
action['Range'] = action['Range'].apply(lambda x: '100%' if re.match(r'^1$',str(x)) else x)
action['Range From'] = action['Range'].apply(lambda x: int(re.search(r'^(\d+)',str(x)).group(1)) if re.match(r'^\d+',str(x)) else 0)
action['Range To'] = action['Range'].apply(lambda x: int(re.search(r'(\d+)%$',str(x)).group(1)) if re.match(r'.*\d+%$',str(x)) else 9999)

final['dummy'] = 'dummy' 
action['dummy'] = 'dummy'
final = pd.merge(final,action,how='inner',on='dummy').query('`Variance to Target X`>=`Range From` & `Variance to Target X`<=`Range To`')
final.rename(columns = {'Variance to Target X':'Variance to Target %'}, inplace=True)
final = final[['Store', 'Variance to Target', 'Variance to Target %', 'Sales', 'Target Value',
               'Quarter', 'Region', 'Target', 'Actions']]