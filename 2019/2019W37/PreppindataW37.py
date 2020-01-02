import pandas as pd
import os 
import re

fruit_scent = ['Apricot','Lemon','Lime','Pineapple','Raspberry']

os.chdir(r'E:/')
mockdata = []
for files in [f for f in os.listdir('.') if re.match('MOCK_DATA.*.csv', f)]:
    dataset = pd.read_csv(files)
    dataset['Month'] = '2019-'+re.search("(\d+)(?=\.csv)",files).group(0).zfill(2)+'-01'
    dataset['Fruit'] = dataset['Scent'].apply(lambda x: 'Fruit' if x in fruit_scent else 'Non-Fruit')
    dataset['Returned Orders'] = dataset['Return'].apply(lambda x: 1 if x else 0)
    mockdata.append(dataset)    
df = pd.concat(mockdata)   
df['All'] = 'All'
df['Total Orders'] = 1
df = df[['All','Fruit','Product Type','Month','Total Orders','Returned Orders']]
df= df.melt(['Total Orders','Returned Orders'], value_name='Type', var_name='ToDrop')
final = df.groupby('Type', as_index=False).agg({'Total Orders':'sum','Returned Orders':'sum'})
final['% Returned'] = round(final['Returned Orders']/final['Total Orders']*100,1) 