import pandas as pd
import re

xlsx = pd.ExcelFile(r"C:\Data\PreppinData\2022W21 Input.xlsx")

temp = []
for sheet in xlsx.sheet_names:
    df = pd.read_excel(xlsx, sheet, skiprows=3)
    df.insert(0,'Shop',sheet)
    temp.append(df)
metrics = pd.concat(temp)   

metrics = metrics.drop([c for c in metrics.columns if re.match('FY.*Q\d', str(c))] + ['Comments'], axis=1)
metrics[['Department', 'Target']] = metrics[['Department', 'Target']].ffill()
metrics = metrics[metrics['Department'].isin(['Orders', 'Returns', 'Complaints'])]
metrics = metrics[metrics['Breakdown'].isin(['% Shipped in 3 days', '% Shipped in 5 days', 
                                             '% Processed in 3 days', '% Processed in 5 days', '# Received'])]
metrics['Breakdown'] = metrics.apply(lambda x: re.sub('(.)\s(.+)', f'\\1 {x["Department"]} \\2', x['Breakdown']), axis=1)
metrics = metrics.drop('Department', axis=1)

metrics = metrics.melt(id_vars=['Shop', 'Target', 'Breakdown'], value_name='Value', var_name='Date').dropna(subset=['Value'])
metrics['Target'] = metrics['Target'].apply(lambda x: float(str(x).replace('>','').replace('%', 'e-2')))
metrics['Value'] = metrics['Value'].astype('float')
metrics['Date'] = metrics['Date'].dt.date

metrics_value = metrics[['Shop', 'Date', 'Breakdown', 'Value']]
metrics_target = metrics[['Shop', 'Date', 'Breakdown', 'Target']].rename(columns={'Target':'Value'})
metrics_target['Breakdown'] = 'Target - ' + metrics_target['Breakdown']

final = pd.concat([metrics_target, metrics_value])
final = final.pivot_table(index=['Shop', 'Date'], columns='Breakdown', values='Value', aggfunc=sum).reset_index()
final = final[['Shop', 'Date', 
               '% Orders Shipped in 3 days', 'Target - % Orders Shipped in 3 days',
               '% Orders Shipped in 5 days', 'Target - % Orders Shipped in 5 days',
               '% Returns Processed in 3 days', 'Target - % Returns Processed in 3 days',
               '% Returns Processed in 5 days', 'Target - % Returns Processed in 5 days',
               '# Complaints Received', 'Target - # Complaints Received']]
