import pandas as pd
from datetime import datetime as dt

rev = pd.read_csv("F:/Data/PD 2021 Wk 26 Input - Sheet1.csv", 
                  parse_dates=['Date'], date_parser=lambda x: dt.strptime(x, '%d/%m/%Y'))
rev = rev.groupby('Destination').apply(lambda x: x.sort_values(['Date'])).reset_index(drop=True)
rev['Date'] = rev['Date'].dt.date
whole = rev.groupby('Date', as_index=False).agg({'Revenue':'sum'})
whole['Destination'] = 'All'

final = pd.concat([rev,whole]).copy()

final['Rolling Avg'] =  final.groupby('Destination')['Revenue'].transform(lambda x: x.rolling(7, 1).mean().shift(-3))
final['Rolling Total'] =  final.groupby('Destination')['Revenue'].transform(lambda x: x.rolling(7, 1).sum().shift(-3))
final['Rolling Avg2'] =  final.groupby('Destination')['Revenue'].transform(lambda x: x.shift(-3).rolling(7, 1).mean())
final['Rolling Total2'] =  final.groupby('Destination')['Revenue'].transform(lambda x: x.shift(-3).rolling(7, 1).sum())

final['Rolling Week Avg'] =  final.apply(lambda x: x['Rolling Avg2'] if pd.isna(x['Rolling Avg'])  else x['Rolling Avg'], axis=1)
final['Rolling Week Total'] =  final.apply(lambda x: x['Rolling Total2'] if pd.isna(x['Rolling Total'])  else x['Rolling Total'], axis=1)

final = final[['Destination', 'Date', 'Rolling Week Avg', 'Rolling Week Total']]
