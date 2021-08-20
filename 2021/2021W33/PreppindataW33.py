import pandas as pd
from datetime import timedelta

xlsx = pd.ExcelFile(r"F:\Data\Allchains Weekly Orders.xlsx")

temp = []
for sheet in xlsx.sheet_names:
    df = pd.read_excel(xlsx,sheet)
    df.insert(0,'Reporting Date', pd.to_datetime(sheet,format='%Y%m%d').date())
    temp.append(df)
order = pd.concat(temp)   

order['Sale Date'] = order['Sale Date'].dt.date

order['Order Max Report Date'] = order['Reporting Date'].groupby(order['Orders']).transform('max')
order['Order Min Report Date'] = order['Reporting Date'].groupby(order['Orders']).transform('min')
order['Order Status'] = order.apply(lambda x: 'New Order' if x['Reporting Date']==x['Order Min Report Date'] else 'Unfulfilled Order', axis=1)

fulfilled = order[order['Reporting Date']==order['Order Max Report Date']].copy()
fulfilled['Reporting Date'] = fulfilled['Order Max Report Date'] + timedelta(weeks=1)
fulfilled = fulfilled[fulfilled['Reporting Date']<=order['Reporting Date'].max()].copy()
fulfilled['Order Status'] = 'Fulfilled'

final = pd.concat([order,fulfilled])[['Order Status', 'Orders', 'Sale Date', 'Reporting Date']].sort_values(['Orders', 'Reporting Date'])
