import pandas as pd
import re
from datetime import datetime as dt

result = pd.read_csv(r'E:/PD 2020 Wk 9 Input - Sheet1.csv', dtype=object)
result = result[~result['Poll'].str.contains('Average')]
result['Sample Type'] = result['Sample'].apply(lambda x: 'Registered Voter' if re.search('RV',x) else 'Likely Voter' if re.search('LV',x) else 'Unknown')

result['End Date'] = result['Date'].apply(lambda x: dt.strptime(re.search(r'(\d+/\d+$)',x).group(1),'%m/%d').date())
result['End Date'] = result['End Date'].apply(lambda x: x.replace(year=(2019 if x.month>10 else 2020)))
cols = result.columns.drop(['Poll','Sample Type','End Date'])
result[cols] = result[cols].apply(pd.to_numeric, errors='coerce')
result = result.drop(['Sample','Date'], axis=1).dropna()

final = result.melt(id_vars=['Poll','Sample Type','End Date'],var_name='Candidate',value_name='Poll Results')
final['Rank'] = final.groupby(['Poll','Sample Type','End Date'], as_index=False)['Poll Results'].rank(ascending=False, method='max').astype(int)
final['Spread'] = final.apply(lambda x: x['Poll Results']*(1 if x['Rank']==1 else -1 if x['Rank']==2 else 0), axis=1)
final['Spread from 1st to 2nd Place'] = final['Spread'].groupby([final['Poll'],final['Sample Type'],final['End Date']]).transform('sum')
final = final.drop('Spread', axis=1).sort_values(['End Date','Poll','Sample Type','Rank'])
