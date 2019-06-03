import pandas as pd

xls = pd.ExcelFile("E:\Week6Input.xlsx")
new_sales = pd.read_excel(xls,"England - Mar 2019") 
price_dtl = pd.read_excel(xls,"Soap Pricing Details") 
com_data = pd.read_excel(xls,"Company Data") 

temp = new_sales['Category'].str.split(' ', n = 1, expand = True) 
new_sales['Type of Soap'] = temp[0]

new_profit = new_sales.merge(price_dtl, on='Type of Soap', how='inner')
new_profit['Profit'] = new_profit['Units Sold']*(new_profit['Selling Price per Unit']-new_profit['Manufacturing Cost per Unit']) 
new_profit['Month'] = 'Mar 19'
new_profit = new_profit[['Month','Country','Category','Profit']].copy()
new_profit = new_profit.groupby(['Month','Country','Category'], as_index=False).agg({'Profit':'sum'})

com_data['Month']=com_data['Month'].dt.strftime('%b %y')
final = com_data.append(new_profit)
