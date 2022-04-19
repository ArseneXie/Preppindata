import pandas as pd
import os
import re

os.chdir('C:\\Data\\PreppinData\\UK Gender Pay Gap Data\\')
dfs = []
for files in os.listdir('.'):
    df = pd.read_csv(files)[['EmployerName', 'EmployerId', 'EmployerSize', 'DiffMedianHourlyPercent']]
    df['Year']= re.search('(\d+)',files).group(0)
    df['Report']= re.search('(\d+ to \d+)',files).group(0)
    dfs.append(df)    
paygap = pd.concat(dfs)  

paygap['Recent Year'] = paygap['Year'].groupby(paygap['EmployerId']).transform('max')
paygap['EmployerName_Temp'] = paygap.apply(lambda x: x['EmployerName'] if x['Year']==x['Recent Year'] else '', axis=1)
paygap['EmployerName'] = paygap['EmployerName_Temp'].groupby(paygap['EmployerId']).transform('max')
paygap['Pay Gap'] = paygap['DiffMedianHourlyPercent'].apply(lambda x:
                                                            "In this organisation, men's and women's median hourly pay is equal." if x==0
                                                            else f"In this organisation, women's median hourly pay is {abs(x)}% {('higher' if x<0 else 'lower')} than men's." )
paygap = paygap[['Year', 'Report', 'EmployerName', 'EmployerId', 'EmployerSize', 'DiffMedianHourlyPercent', 'Pay Gap']]
