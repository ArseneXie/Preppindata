import pandas as pd
import numpy as np
import re

stats = pd.read_csv("C:\\Data\\PreppinData\\Southend Stats.csv", sep='\s+')
stats = stats.rename(columns={stats.columns[-2]:'Pts'})
stats= stats.sort_values(by='SEASON')
stats['Special Circumstances'] = stats.apply(lambda x: 'Incomplete' if x['SEASON']==stats['SEASON'].max() else 
                                             'Abandoned due to WW2' if x['SEASON'][0:4]=='1939' else 'N/A', axis=1)
stats['POS'] = stats.apply(lambda x: x['POS'] if x['Special Circumstances']=='N/A' else None, axis=1)
stats['League Num'] = stats['LEAGUE'].apply(lambda x: 0 if x=='FL-CH' else 5 if x=='NAT-P' else int(re.search('(\d)',x).group(1)))
stats['Outcome Key'] = stats['League Num'] - stats['League Num'].shift(-1) 
stats['Outcome'] = stats['Outcome Key'].apply(lambda x: 'Promoted' if x>0 else 'Relegated' if x<0 else 'Same League' if x==0 else None)

stats.index = stats['SEASON'].apply(lambda x: int(x[0:4]))
stats = stats.reindex(np.arange(stats.index.min(), stats.index.max() + 1)).rename_axis('Year').reset_index()
stats['SEASON'] = stats['Year'].apply(lambda x: f'{x}-{str(x+1)[-2:]}')
stats['Special Circumstances'] = stats.apply(lambda x: x['Special Circumstances'] if pd.notna(x['Special Circumstances']) else
                                             'WW1' if x['Year']<1939 else 'WW2', axis=1)
stats = stats[['SEASON', 'Outcome', 'Special Circumstances', 'LEAGUE', 'P', 'W', 'D', 'L', 'F', 'A', 'Pts', 'POS']]
