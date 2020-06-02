import pandas as pd
import random

xlsx = pd.ExcelFile("F:/Data/2020W22 Input.xlsx")

ttl = pd.read_excel(xlsx,'Total Market')
comp = pd.read_excel(xlsx,'Companies')
scent = pd.read_excel(xlsx,'Scents')

march_ttl = ttl['March Sales'][0]
april_ttl = march_ttl*(1+ttl['Growth'][0])

comp['random1'] = comp.apply(lambda x:random.random(),axis=1)
comp['random2'] = comp.apply(lambda x:random.random(),axis=1)
comp['March'] = march_ttl*comp['random1']/comp['random1'].sum()
comp['randomRank'] = comp['random2'].rank().astype(int)
comp['ChangeBps'] = comp['randomRank'].apply(lambda x: -30+x*10)
comp['April'] = april_ttl*(comp['random1']/comp['random1'].sum()+comp['ChangeBps']/10000)

final = comp[['Company','March','April']].melt(id_vars='Company', value_name='CM Sales', var_name='Month')
final['dummy'] = 0
scent['dummy'] = 0
final = pd.merge(final, scent, on='dummy')

final['random1'] = final.apply(lambda x:random.random(),axis=1)
final['randomttl'] = final['random1'].groupby([final['Company'],final['Month']]).transform('sum')
final['Sales'] = final.apply(lambda x: x['CM Sales']*x['random1']/x['randomttl'],axis=1)
final = final[['Company', 'Month', 'Soap Scent', 'Sales']]
