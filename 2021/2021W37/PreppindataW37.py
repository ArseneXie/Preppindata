import pandas as pd
import numpy as np

xlsx = pd.ExcelFile(r"F:\Data\2021 Week 37 Input.xlsx")

contract = pd.read_excel(xlsx,'Contract Details')
final = contract.iloc[np.repeat(np.arange(len(contract)), list(contract['Contract Length (months)']))].copy()
final['rownum'] = final.groupby(['Name'])['Start Date'].rank(method='first')
final['Payment Date'] = final.apply(lambda x: (x['Start Date']+pd.DateOffset(months=x['rownum']-1)).date(), axis=1) 
final['Cumulative Monthly Cost'] = final['Monthly Cost']*final['rownum'] 
final = final[['Name', 'Payment Date', 'Monthly Cost', 'Cumulative Monthly Cost']]
