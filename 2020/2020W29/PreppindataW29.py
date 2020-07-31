import pandas as pd
import re

xlsx = pd.ExcelFile("F:/Data/Attendee List.xlsx")

attd = pd.read_excel(xlsx,'Attendee List')   
attd['Currency'] = attd['Country'].apply(lambda x: 'USD' if x=='United States' else
                                         'CAD' if x=='Canada' else
                                         'MXN' if x=='Mexico' else
                                         'GBP' if x=='United Kingdom' else 'EUR') 
attd['Lower Company'] = attd['Email'].apply(lambda x: re.search('(?<=@)([^\.]*)(?=\.)',x).group(1).lower())

mngr = pd.read_excel(xlsx,'Account Manager').rename(columns={'Company List':'Company Name'})
mngr_order = {mgr:idx+1 for idx, mgr in enumerate(list(set(mngr['Account Manager'].to_list())))}
mngr['Order'] = mngr['Account Manager'].apply(lambda x: mngr_order[x])
mngr['Lower Company'] = mngr['Company Name'].str.lower()  


rate = pd.read_excel(xlsx,'Exchange Rates').drop('GBP', axis=1)
rate['Currency'] = rate['Currency'].apply(lambda x: x[:3])
rate = pd.concat([rate, pd.DataFrame({'Currency': ['GBP'], 'Rate': [1]})])

finalA = attd.merge(mngr, on='Lower Company').drop('Lower Company',axis=1)
finalA = finalA.merge(rate, on='Currency')
finalA['Ticket Price Local'] = finalA['Ticket Price (£)']*finalA['Rate']
finalA = finalA.drop(['Ticket Price (£)','Rate'], axis=1)

finalB = finalA.copy()
finalB['Money Gain/Loss'] = finalB.apply(lambda x: (-1 if x['Refund Type']=='Full Refund' else 1)*x['Ticket Price Local'], axis=1)
finalB = finalB.groupby(['Country','Currency'], as_index=False).agg({'Money Gain/Loss':'sum'})
