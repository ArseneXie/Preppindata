import pandas as pd
import re
import numpy as np

xlsx = pd.ExcelFile(r"C:\Data\PreppinData\7 letter words.xlsx")

scores = pd.read_excel(xlsx,'Scrabble Scores')
scores['Points'] = scores['Scrabble'].apply(lambda x: int(re.search('^(\d+)',x).group(1)))
scores['TileFreq'] = scores['Scrabble'].str.extract('(?<=:\s)(.*)')
scores = pd.concat([scores['Points'], 
                   pd.DataFrame([map(str.strip, x) for x in scores['TileFreq'].str.split(',').values.tolist()])], 
                   axis=1, sort=False)
scores = scores.melt(id_vars='Points', value_name='TileFreq', var_name='ToDrop').dropna().drop('ToDrop', axis=1)    
scores['Tile'] = scores['TileFreq'].apply(lambda x: re.search('^(\w+)',x).group(1))
scores['Frequency'] = scores['TileFreq'].apply(lambda x: float(re.search('(\d+)$',x).group(1)))
scores['LN Chance'] = np.log(scores['Frequency'] / scores['Frequency'].sum())

words = pd.read_excel(xlsx,'7 letter words') 
words = pd.concat([words, 
                   pd.DataFrame([map(str.upper, x) for x in words['7 letter word'].str.split('').values.tolist()])], 
                   axis=1, sort=False)
words = words.melt(id_vars='7 letter word', value_name='Letter', var_name='ToDrop').drop('ToDrop', axis=1).replace('', np.NaN).dropna()
words['Letter Count'] = words['Letter'].groupby([words['7 letter word'],words['Letter']]).transform('count')

final = pd.merge(words, scores, left_on='Letter', right_on='Tile')
final = final[final['Frequency']>=final['Letter Count']]
final['Match Letter'] = final['Letter'].groupby(final['7 letter word']).transform('count')
final = final[final['Match Letter']==7]

final = final.groupby('7 letter word', as_index=False).agg({'Points':'sum', 'LN Chance':'sum'}).rename(columns={'Points':'Total Points'})
final['% Chance'] = np.exp(final['LN Chance'])
final['% Chance Temp'] = round(final['% Chance'],15)
final['Likelihood Rank'] = final['% Chance Temp'].rank(method='dense',ascending=False).astype(int)
final['Points Rank'] = final['Total Points'].rank(method='dense',ascending=False).astype(int)
final = final[['Points Rank', 'Likelihood Rank', '7 letter word', '% Chance', 'Total Points']]
