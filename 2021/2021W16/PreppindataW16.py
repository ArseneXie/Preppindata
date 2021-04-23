import pandas as pd
import os

os.chdir(r'F:\Data\2021W13')
mergedata = []
for files in [f for f in os.listdir('.')]:
    dataset = pd.read_csv(files)
    mergedata.append(dataset)    
df = pd.concat(mergedata)
df = df[(df['Position']!='Goalkeeper') & (df['Appearances']>0)].rename(columns={'Goals':'Total Goals'})  
df[['Penalties scored','Freekicks scored']] = df[['Penalties scored','Freekicks scored']].fillna(value=0).astype('int64')
df['Open Play Goals'] = df['Total Goals'] - df['Penalties scored'] - df['Freekicks scored']
df = df.groupby(['Name', 'Position'], as_index=False).agg({'Appearances':'sum', 'Open Play Goals':'sum',
                                                           'Total Goals':'sum', 'Headed goals':'sum',
                                                           'Goals with right foot':'sum', 'Goals with left foot':'sum'})
df[['Headed goals','Goals with right foot','Goals with left foot']] = df[['Headed goals','Goals with right foot','Goals with left foot']].astype('int64')
df['Open Play Goals / Game'] = (df['Open Play Goals'] / df['Appearances'] ).astype('float')

finalA = df.copy()
finalA['Rank'] = finalA['Open Play Goals'].rank(method='min', ascending=False).astype(int)
finalA = finalA[finalA['Rank']<=20][['Rank', 'Name', 'Position', 'Open Play Goals', 'Appearances', 'Open Play Goals / Game', 
                                     'Headed goals', 'Goals with right foot', 'Goals with left foot', 'Total Goals']]
finalB = df.copy()
finalB['Rank'] = finalB.groupby('Position')['Open Play Goals'].rank(method='min', ascending=False).astype(int)
finalB = finalB[finalB['Rank']<=20][['Rank', 'Name', 'Position', 'Open Play Goals', 'Appearances', 'Open Play Goals / Game', 
                                     'Headed goals', 'Goals with right foot', 'Goals with left foot', 'Total Goals']]
