import pandas as pd

task_list = ['Scope', 'Build', 'Deliver']
final = pd.read_excel(pd.ExcelFile("F:/Data/PD 2021 Wk 18 Input.xlsx"),sheet_name=0).rename(
    columns={'Completed In Days from Scheduled Date':'Days Difference to Schedule'})

final['Completed Date'] = final.apply(lambda x: x['Scheduled Date'] + pd.DateOffset(days=x['Days Difference to Schedule']), axis=1)
final['Completed Weekday'] = final['Completed Date'].dt.strftime('%A')
final['Scheduled Date'] = final['Scheduled Date'].dt.date
final['Completed Date'] = final['Completed Date'].dt.date

for tk in task_list:
    final[f'For {tk} Date'] = final.apply(lambda x: str(x['Completed Date']) if x['Task']==tk else '', axis=1)
    final[f'{tk} Date'] = final[f'For {tk} Date'].groupby([final['Project'],final['Sub-project']]).transform('max')
final['Scope to Build Time'] = final.apply(lambda x: (pd.to_datetime(x['Build Date'])-pd.to_datetime(x['Scope Date'])).days, axis=1)    
final['Build to Delivery Time'] = final.apply(lambda x: (pd.to_datetime(x['Deliver Date'])-pd.to_datetime(x['Build Date'])).days, axis=1)   

final = final[['Project', 'Sub-project', 'Owner', 'Scheduled Date', 'Completed Date', 'Completed Weekday',
               'Task', 'Scope to Build Time', 'Build to Delivery Time', 'Days Difference to Schedule']].copy()
