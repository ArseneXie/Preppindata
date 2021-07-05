import pandas as pd
import re

xlsx = pd.ExcelFile("F:/Data/2021W25 Input.xlsx")
gen1 = pd.read_excel(xlsx,sheet_name='Gen 1')[['#','Name']].dropna()

evogroup = pd.read_excel(xlsx,sheet_name='Evolution Group')
evogroup['#']=evogroup['#'].apply(lambda x: int(x.strip()))
evogroup = evogroup[(evogroup['Starter?']==0) & (evogroup['Legendary?']==0)][['#','Evolution Group']]

gen1g = pd.merge(gen1, evogroup, on='#').drop('#', axis=1)

evo = pd.read_excel(xlsx,sheet_name='Evolutions')[['Evolving from', 'Evolving to']]

df = pd.concat([
    pd.merge(evo, gen1g, left_on='Evolving from', right_on='Name')[['Evolution Group','Evolving to']].rename(
        columns={'Evolving to':'Pokemon'}),
    pd.merge(evo, gen1g, left_on='Evolving to', right_on='Name')[['Evolution Group','Evolving from']].rename(
        columns={'Evolving from':'Pokemon'})]).drop_duplicates()

mega = pd.concat([pd.read_excel(xlsx,sheet) for sheet in ['Mega Evolutions', 'Alolan', 'Galarian', 'Gigantamax']])
mega['Name'] = mega['Name'].apply(lambda x: re.sub('^\w+\s','',x))
mega = mega.drop_duplicates()

df['Check'] = df['Pokemon'].isin(list(mega['Name'])).astype(int)
df['Group Check'] = df['Check'].groupby(df['Evolution Group']).transform('sum') 
df = df[df['Group Check']==0][['Evolution Group', 'Pokemon']].copy()

unatt = pd.read_excel(xlsx,sheet_name='Unattainable in Sword & Shield').rename(columns={'Name':'Evolution Group'})
anime = pd.read_excel(xlsx,sheet_name='Anime Appearances')

df = pd.merge(df, unatt, on='Evolution Group')
df = pd.merge(df, anime, on='Pokemon')
df = df.groupby('Evolution Group', as_index=False).agg(Appearances=('Episode','nunique'))
df['The Worst Pokemon'] = df['Appearances'].rank(method='min').astype(int)
df = df[['The Worst Pokemon', 'Evolution Group', 'Appearances']].sort_values('Appearances')
