import pandas as pd

xls = pd.ExcelFile("E:/PD Wk 44 Input.xlsx")
sales = pd.read_excel(xls,'Store Sales')
members = pd.read_excel(xls,'Team Member Days')

sales = sales.melt(id_vars='Date', value_name='Store Sales', var_name='Store')

final = pd.merge(sales,members,how='inner',on=['Store','Date'])
final['Estimated Sales From Staff Member'] = final['Store Sales']/final['Team Member'].groupby([final['Store'],final['Date']]).transform('count')
final = final.groupby(['Store','Team Member'], as_index=False).agg({'Estimated Sales From Staff Member':'mean'}).round(2)
final['Rank'] = final.groupby('Store')['Estimated Sales From Staff Member'].rank(ascending=False).astype(int)
