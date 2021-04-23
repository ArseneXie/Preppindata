import pandas as pd

xlsx = pd.ExcelFile("F:/Data/Menu and Orders.xlsx")

menu = pd.read_excel(xlsx,sheet_name='MENU')
temp = []
for i in [0,3,6]:
    df = menu[menu.columns[i:i+3]].copy().dropna()
    df.columns = ['Name', 'Price', 'ID']
    df['Type'] = menu.columns[i].lower()
    temp.append(df)
menu = pd.concat(temp)   
menu['ID'] = menu['ID'].astype(int).astype(str)

order = pd.read_excel(xlsx,sheet_name='Order',dtype=str)
order = pd.concat([order.drop('Order', axis=1), 
                   pd.DataFrame([map(str.strip, x) for x in order['Order'].str.split('-').values.tolist()])],
                  axis=1, sort=False)
order = order.melt(id_vars=['Customer Name', 'Order Date'],value_name='ID', var_name='toDrop').drop('toDrop', axis=1).dropna()
order['Weekday'] = pd.to_datetime(order['Order Date'], format='%Y-%m-%d').dt.strftime('%A')

df = pd.merge(order[['Customer Name', 'Weekday', 'ID']], menu[['ID', 'Price']], on='ID')
df['Price'] = df.apply(lambda x: x['Price']*(0.5 if x['Weekday']=='Monday' else 1), axis=1)

finalA = df.groupby('Weekday', as_index=False).agg({'Price':'sum'})
finalB = df.groupby('Customer Name', as_index=False).agg({'ID':'count'}).rename(columns={'ID':'Count Items'})
finalB = finalB[finalB['Count Items'] == max(finalB['Count Items'])]
