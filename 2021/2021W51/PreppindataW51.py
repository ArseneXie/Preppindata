import pandas as pd

df = pd.read_csv("C:\\Data\\PreppinData\\2021W51 Input.csv", 
                     parse_dates=['Order Date'], date_parser=lambda x: pd.to_datetime(x, format='%d/%m/%Y'))
df['Order Date'] = df['Order Date'].dt.date
temp = df['OrderID'].str.split('-', n = 1, expand = True) 
df['Store'] = temp[0] 
df['OrderID'] = temp[1]
df['Returned'] = df['Return State'].apply(lambda x: int(pd.notna(x)))
df['Unit Price'] = df['Unit Price'].apply(lambda x: float(x[1:])) 
df['Sales'] = df['Unit Price']*df['Quantity']
df['Product'] = df['Product Name'].str.lower()

for dim in ['Store', 'Customer', 'Product']:
    df[f'{dim} First Order'] = df['Order Date'].groupby(df[dim]).transform('min')
    df[f'{dim}ID'] = df[[f'{dim} First Order',dim]].apply(tuple,axis=1).rank(method='dense',ascending=True).astype(int)

fact = df[['StoreID', 'CustomerID', 'OrderID', 'Order Date', 'ProductID', 'Returned', 'Quantity', 'Sales']].copy()

store = df[['StoreID', 'Store', 'Store First Order']].drop_duplicates().copy()
store = store.rename(columns={'Store First Order':'First Order'}).sort_values('StoreID')

customer = df.groupby(['CustomerID', 'Customer', 'Customer First Order'], as_index=False).agg({'OrderID':'nunique', 'Product':'count', 'Returned':'sum'})
customer['Return %'] = round(customer['Returned']/customer['Product'], 2)
customer = customer.rename(columns={'Customer First Order':'First Order', 'OrderID':'Number of Orders'})
customer = customer[['CustomerID', 'Customer', 'Return %', 'Number of Orders', 'First Order']].sort_values('CustomerID')

product = df[['ProductID', 'Category', 'Sub-Category', 'Product Name', 'Unit Price', 'Product First Order']].drop_duplicates().copy()
product = product.rename(columns={'Product First Order':'First Sold'}).sort_values('ProductID')
