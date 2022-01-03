import pandas as pd
import re

xlsx = pd.ExcelFile(r"C:\Data\PreppinData\PD 2021 Wk 52 Input.xlsx")

resp = pd.read_excel(xlsx, 'Department Responsbile')
resp = resp.groupby('Department')['Keyword'].apply(list).reset_index(name='Keyword List') 
resp['Dummy'] = 1

comp = pd.read_excel(xlsx, 'Complaints')
comp['Complaints per person'] = comp['Complaint'].groupby(comp['Name']).transform('count')
comp['ID'] = comp.index
comp['Dummy'] = 1

final = pd.merge(comp, resp, on='Dummy')
final['Match'] = final.apply(lambda x: [kw.lower() for kw in x['Keyword List'] if re.match(f'.*{kw.lower()}.*', x['Complaint'])], axis=1)
final['Match Count'] = final['Match'].apply(lambda x: len(x)) 
final['Complaint Match'] = final['Match Count'].groupby(final['ID']).transform('sum')
final['Department'] = final.apply(lambda x: 'Unknown' if x['Complaint Match']==0 else x['Department'], axis=1)
final['Complaint causes'] = final.apply(lambda x: 'other' if x['Complaint Match']==0 else ', '.join(x['Match']), axis=1)
final = final[((final['Complaint Match']==0) | (final['Match Count']>0))]
final = final[['Complaint', 'Complaint causes', 'Department', 'Name', 'Complaints per person']].drop_duplicates()
