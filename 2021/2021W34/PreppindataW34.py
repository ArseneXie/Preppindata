import pandas as pd

xlsx = pd.ExcelFile(r"F:\Data\2021 Week 34 Input.xlsx")

sales = pd.read_excel(xlsx,'Employee Sales')
sales = sales.melt(id_vars=['Store', 'Employee'], var_name='Month', value_name='Monthly Sales')
sales = sales.groupby([sales['Store'],sales['Employee']])['Monthly Sales'].apply(list).reset_index()
sales['Avg monthly Sales'] = sales['Monthly Sales'].apply(lambda x: round(sum(x)/len(x)))

target = pd.read_excel(xlsx,'Employee Targets')
storefix_pt = {'Bristol':'^B.*', 'Stratford':'^S.*', 'Wimbledon':'.imble.*', 'York':'^Y.*'}
target['Store'] = target['Store'].replace(list(storefix_pt.values()), list(storefix_pt.keys()), regex = True)

final = pd.merge(sales, target, on=['Store', 'Employee'])
final = final[final['Avg monthly Sales']<final['Monthly Target']*0.9]
final['% of months target met'] = final.apply(lambda x: round(len([s for s in x['Monthly Sales'] if s>=x['Monthly Target']])/
                                                              len(x['Monthly Sales'])*100), axis=1)
final = final[['Store', 'Employee', 'Avg monthly Sales', '% of months target met', 'Monthly Target']]
