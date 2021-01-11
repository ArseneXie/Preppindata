import pandas as pd
import re

bikefix_pt = {'Mountain':'^M.*', 'Gravel':'^G.*', 'Road':'^R.*'}

df = pd.read_csv(r'F:/Data/PD 2021 Wk 1 Input - Bike Sales.csv')
df['Store'] = df['Store - Bike'].apply(lambda x: re.search('^(\w+)',x).group(1))
df['Bike'] = df['Store - Bike'].apply(lambda x: re.search('(\w+)$',x).group(1))

for correct, pattern in bikefix_pt.items():
    df['Bike'] = df['Bike'].replace(to_replace = pattern, value = correct, regex = True)

df['Date'] = df['Date'].apply(lambda x: pd.to_datetime(x,format='%d/%m/%Y').date())
df['Quarter'] = df['Date'].apply(lambda x: (x.month-1)//3+1)
df['Day of Month'] = df['Date'].apply(lambda x: x.day)

final = df[df['Order ID']>10][['Quarter', 'Day of Month', 'Store', 'Bike', 'Order ID', 'Customer Age', 'Bike Value', 'Existing Customer?']].copy()
