import pandas as pd
import re

xlsx = pd.ExcelFile("F:/Data/PD 2021 Wk 21 Input.xlsx")

temp = []
for sheet in xlsx.sheet_names:
    df = pd.read_excel(xlsx,sheet)
    df.insert(0,'Month',re.search('(\d+)',sheet).group(0))
    temp.append(df)
sales = pd.concat(temp)   
sales['Date'] = sales.apply(lambda x: pd.to_datetime(f"2021-{x['Month']}-{x['Day of Month']}", format='%Y-%m-%d').date(), axis=1)
sales['New Trolley Inventory'] = sales['Month'].apply(lambda x: int(x)>=6)
sales['Product'] = sales['Product'].apply(lambda x: re.search('^([^-]+)',x).group(0).strip())
sales['Destination'] = sales['Destination'].str.strip()
sales['Price'] = sales['Price'].apply(lambda x: float(re.search('([\d\.]+)',x).group(0))) 
sales['Average Price per Product'] = sales['Price'].groupby(sales['Product']).transform('mean')
sales['Variance'] = sales['Price'] - sales['Average Price per Product']
sales['Variance Rank by Destination'] = sales.groupby(['Destination','New Trolley Inventory'])['Variance'].rank(method='dense',ascending=False).astype(int)
sales = sales[sales['Variance Rank by Destination']<=5][['New Trolley Inventory','Variance Rank by Destination','Variance','Average Price per Product',
                                                        'Date','Product','first_name', 'last_name', 'email','Price', 'Destination']]
sales = sales.sort_values(by=['Destination', 'New Trolley Inventory', 'Variance Rank by Destination'])
