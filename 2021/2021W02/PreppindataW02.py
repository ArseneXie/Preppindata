import pandas as pd
from datetime import datetime as dt
import re

df = pd.read_csv(r'F:/Data/PD 2021 Wk 2 Input - Bike Model Sales.csv', parse_dates=['Order Date','Shipping Date'],
                 date_parser=lambda x: dt.strptime(x, '%d/%m/%Y') if re.match('\d+/\d+/\d+', x) else dt.strptime(x, '%d-%m-%Y'))

df['Brand'] = df['Model'].apply(lambda x: re.sub('[^A-Z]','',x))
df['Order Value'] = df['Quantity']*df['Value per Bike']
df['Days to Ship'] = df.apply(lambda x: (x['Shipping Date'] - x['Order Date']).days, axis=1)

finalA = df.groupby(['Brand','Bike Type'], as_index=False).agg({'Quantity':'sum', 'Order Value':'sum', 'Value per Bike':'mean'})
finalA = finalA.rename(columns={'Quantity':'Quantity Sold', 'Value per Bike':'Avg Bike Value per Brand'})
finalA['Avg Bike Value per Brand'] = round(finalA['Avg Bike Value per Brand'], 1)

finalB = df.groupby(['Brand','Store'], as_index=False).agg({'Quantity':'sum', 'Order Value':'sum', 'Days to Ship':'mean'})
finalB = finalB.rename(columns={'Quantity':'Total Quantity Sold', 'Order Value':'Total Order Value', 'Days to Ship':'Avg Days to Ship'})
finalB['Avg Days to Ship'] = round(finalB['Avg Days to Ship'], 1)
