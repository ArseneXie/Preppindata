import pandas as pd
import os
import re

os.chdir(r'E:/PD15/')
mergedata = []
for files in [f for f in os.listdir('.') if re.match('.*Stock Purchases.csv', f)]:
    dataset = pd.read_csv(files)
    dataset['Region']= re.search('^\w+(?=\s)',files).group(0)
    mergedata.append(dataset)    
df = pd.concat(mergedata)   

total = ((df.groupby(['Stock','Region']).agg({'Sales':'sum'}).rename(columns={'Sales': 'Total Regional Sales'}))
        .join(df.groupby(['Stock']).agg({'Sales':'sum'})).rename(columns={'Sales': 'Total Sales'})
        .reset_index()
        )

final = pd.merge(df, total, how='inner', on=['Region','Stock'])
final = final[final['Sales']<final['Total Regional Sales']]
final['% of Total Sales'] = final['Sales']/final['Total Sales']*100
final['% of Total Regional Sales'] = final['Sales']/final['Total Regional Sales']*100

#check = final.loc[(final['Region']=='South') & (final['Customer ID']==1)]
