import pandas as pd

sales = pd.read_csv("F:\\Data\\PD 2021 Wk 31 Input.csv")
sales = sales[sales['Status'] != 'Return to Manufacturer'][['Store', 'Item', 'Number of Items']].copy() 
sales['Item sold per store'] = sales['Number of Items'].groupby(sales['Store']).transform('sum')
sales = sales.pivot_table(index=['Store', 'Item sold per store'], columns='Item', values='Number of Items', aggfunc=sum).reset_index()
sales = sales[['Store', 'Wheels', 'Tyres', 'Saddles', 'Brakes', 'Item sold per store']]
