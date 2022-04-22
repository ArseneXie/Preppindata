import pandas as pd
import datetime
import numpy as np
from dateutil.relativedelta import relativedelta

today = datetime.date(2022, 4, 13)

contract = pd.read_excel(pd.ExcelFile(r"C:\Data\PreppinData\Rental Contracts.xlsx"))
contract['Contract Length'] = contract.apply(lambda x: (x['Contract End'].year - x['Contract Start'].year)*12 + 
                                             (x['Contract End'].month - x['Contract Start'].month), axis=1)
contract['Months Until Expiry'] = contract.apply(lambda x: (x['Contract End'].year - today.year)*12 + 
                                             (x['Contract End'].month - today.month), axis=1)

price = pd.read_excel(pd.ExcelFile(r"C:\Data\PreppinData\Office Space Prices.xlsx"))

final = pd.merge(contract, price, on=['City', 'Office Size'])
final = final.iloc[np.repeat(np.arange(len(final)), list(final['Contract Length']))].reset_index(drop=True)
final['Seq'] = final.groupby(['ID'])['ID'].rank(method='first').astype(int)
final['Month Divider'] = final.apply(lambda x: x['Contract Start'] + relativedelta(months=x['Seq']-1),axis=1) 
final['Cumulative Monthly Cost'] = final['Rent per Month']*final['Seq'] 

output1 = final[['Cumulative Monthly Cost', 'ID', 'Country', 'City', 'Address', 'Company', 'Office Size',
       'Contract Start', 'Contract End', 'Contract Length', 'Months Until Expiry', 'People', 'Per Person', 
       'Rent per Month', 'Month Divider']]

final['Year'] = final['Month Divider'].apply(lambda x: x.year)
final['EoY and Current'] = final.apply(lambda x: x['Rent per Month'] if x['Month Divider'].date().replace(day=1)<=today.replace(day=1) else 0, axis=1)

output2 = final.groupby('Year', as_index=False).agg({'EoY and Current':'sum'})
output2['EoY and Current'] = output2.apply(lambda x: x['EoY and Current'] if x['Year']<=today.year else None, axis=1)
