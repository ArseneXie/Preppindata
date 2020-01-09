import pandas as pd
import re

df = pd.read_csv(r'E:/PD 2020 WK 1 Input - Sheet1.csv')

df['LV1'] = df['Item'].apply(lambda x: re.search(r'(\d+)\.',x).group(1))
df['LV2'] = df['Item'].apply(lambda x: re.search(r'\.(\d+)(\.|\s)',x).group(1) if re.search(r'\.(\d+)(\.|\s)',x) else '0')
df['LV3'] = df['Item'].apply(lambda x: re.search(r'(?:\d+\.){2}(\d+)(\.|\s)',x).group(1) if re.search(r'(?:\d+\.){2}(\d+)(\.|\s)',x) else '0')
df['Level'] = df.apply(lambda x: 1 if x['LV2']=='0' else 2 if x['LV3']=='0' else 3, axis=1)

df['Profit'] =  df['Profit'].fillna(df.groupby('LV1')['Profit'].transform('sum'))
df['Profit'] =  df.apply(lambda x: None if x['Level']==2 else x['Profit'], axis=1)
df['Profit'] =  df['Profit'].fillna(df.groupby(['LV1','LV2'])['Profit'].transform('sum'))
df['Item'] =  df.apply(lambda x: ' '*((x['Level']-1)*5)+x['Item'], axis=1)

final = df[['Item','Profit']].copy()
