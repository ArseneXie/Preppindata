import pandas as pd
import re
import numpy as np

xls = pd.ExcelFile("E:/Preppin Data Final 161119.xlsx")
order = pd.read_excel(xls,'Orders',dtype=str)
batch = pd.read_excel(xls,'Batches',dtype=str)
complaint = pd.read_excel(xls,'Complaints ')

complaint['Order Number'] = complaint['Complaint'].apply(lambda x: re.search(r'\b(\d{5})\b',x).group(1))
complaint['Customer ID'] = complaint['Complaint'].apply(lambda x: re.search(r'\b(\d{4})\b',x).group(1))
complaint['Item Number'] = complaint['Complaint'].apply(lambda x: re.search(r'\b(\d{1})\b(?!\sday)',x).group(1))
complaint = (complaint.drop('Complaint',axis=1)).drop_duplicates()

data = pd.merge(order, complaint, how='left', on=['Order Number','Customer ID','Item Number'],indicator='Complaint Flag') 
data = pd.merge(data, batch, how='inner', on=['Batch Number','Product','Scent']) 
data['Item Sold'] = 1
data['Complaint Flag'] = data['Complaint Flag'].apply(lambda x: 1 if x=='both' else 0)
data['Batch Sold'] = data['Item Sold'].groupby(data['Batch Number']).transform('sum')
data['Batch Complaint'] = data['Complaint Flag'].groupby(data['Batch Number']).transform('sum')
data['Recall Batch'] = data.apply(lambda x: 1 if x['Batch Complaint']/x['Batch Sold']>=0.2 else 0,axis=1)
data['Refund Items Only'] = data.apply(lambda x: float(x['Price'])*(1-x['Recall Batch'])*x['Complaint Flag'],axis=1)
data['Recall Whole Batch'] = data.apply(lambda x: float(x['Price'])*x['Recall Batch']*int(x['Size of Order']),axis=1)

lost = data.groupby(['Batch Number'], as_index=False).agg({'Refund Items Only':'sum','Recall Whole Batch':'max'})
lost['Total Amount Lost'] = lost['Refund Items Only']+lost['Recall Whole Batch']
lost_sum = lost.agg({'Total Amount Lost':'sum',
                     'Refund Items Only':'sum',
                     'Recall Whole Batch':'sum'}).reset_index(name='Money Lost').rename(columns={'index':'Type of Refund'})

remain = data.replace({'Scent': {np.nan: ''}}).groupby(['Batch Number','Product','Scent'], as_index=False).agg(
        {'Item Sold':'sum','Size of Order':'max','Recall Batch':'max'})
remain = remain.query('`Recall Batch`==0')
remain['Size of Order'] = remain['Size of Order'].astype(int)
remain_sum = remain.groupby(['Product','Scent'], as_index=False).agg({'Size of Order':'sum','Item Sold':'sum'})
remain_sum['Stock Remaining'] = remain_sum['Size of Order'] - remain_sum['Item Sold']
remain_sum = remain_sum.drop(['Size of Order','Item Sold'],axis=1).replace({'Scent': {'': np.nan}})
