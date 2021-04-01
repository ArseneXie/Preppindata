import pandas as pd
import re

tourism = pd.read_csv("F:\\Data\\Tourism Input.csv")
tourism = tourism[(tourism['Unit-Detail']=='Tourists') & (tourism['Series-Measure']!='Total tourist arrivals')]
tourism = tourism.melt(id_vars=[c for c in tourism.columns if not re.match('\w{3}-\d{2}',c)],
                          value_name='Original Tourists', var_name='Month')
tourism['Original Tourists'] = tourism['Original Tourists'].apply(lambda x: pd.to_numeric(x, errors='coerce'))
tourism = tourism.dropna()
tourism['Month'] = tourism['Month'].apply(lambda x: pd.to_datetime(x,format='%b-%y').date())
tourism['Breakdown'] = tourism.apply(lambda x: re.search('(?:.*/){3}\s(.*)',x['Hierarchy-Breakdown']).group(1) if re.search('(?:.*/){3}\s(.*)',x['Hierarchy-Breakdown']) 
                                     else re.search('(?:from|-)\s(.*)',x['Series-Measure']).group(1), axis=1) 
tourism['Country'] = tourism.apply(lambda x: re.search('from\s(?:the\s)*(.*)',x['Series-Measure']).group(1) if re.search('(?:.*/){3}\s(.*)',x['Hierarchy-Breakdown']) 
                                   else 'Unknown', axis=1) 

tourism['Modifier'] = tourism.apply(lambda x: 0 if x['Country']=='Unknown' else -1*x['Original Tourists'], axis=1)
tourism['Breakdown-Modifier'] = tourism['Modifier'].groupby([tourism['Breakdown'],tourism['Month']]).transform('sum')
tourism['Number of Tourists'] = tourism.apply(lambda x: x['Original Tourists'] + (x['Breakdown-Modifier'] if x['Country']=='Unknown' else 0), axis=1)

final = tourism[['Month', 'Breakdown', 'Country', 'Number of Tourists']].copy()
