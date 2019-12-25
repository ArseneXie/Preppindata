import pandas as pd
import os
import re

os.chdir(r'E:/InputW45/')
mergedata = []
for files in [f for f in os.listdir('.') if re.match('\w+\s\w+.csv', f)]:
    dataset = pd.read_csv(files)
    dataset['Store']= re.search('^\w+(?=\s)',files).group(0)
    dataset['Weekday']= re.search('\w+(?=\.)',files).group(0)
    mergedata.append(dataset)    
sales = pd.concat(mergedata).drop_duplicates()   

dates = pd.read_csv('Dates.csv')
dates['Weekday'] = dates['Dates'].apply(lambda x: re.search('^\w+(?=\s)',x).group(0))

rowdata = pd.merge(sales,dates,how='inner',on='Weekday')

final1 = rowdata.groupby(['Store','Scent']).agg({'Sales Value':'sum', 'Sales Volume':'sum'})
final1['Scent % of Store Sales Volumes'] = final1['Sales Volume'].groupby(level=0).apply(lambda x: round(x/float(x.sum()),2))
final1['Scent % of Store Sales Values'] = final1['Sales Value'].groupby(level=0).apply(lambda x: round(x/float(x.sum()),2))
final1 = final1.reset_index(drop=False).drop(['Sales Volume','Sales Value'],axis=1)

final2 = rowdata.groupby(['Store','Dates']).agg({'Sales Value':'sum', 'Sales Volume':'sum'})
final2['Weekday % of Store Sales Volumes'] = final2['Sales Volume'].groupby(level=0).apply(lambda x: round(x/float(x.sum()),2))
final2['Weekday % of Store Sales Values'] = final2['Sales Value'].groupby(level=0).apply(lambda x: round(x/float(x.sum()),2))
final2 = final2.reset_index(drop=False).drop(['Sales Volume','Sales Value'],axis=1)
