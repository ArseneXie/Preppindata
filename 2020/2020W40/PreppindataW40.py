import pandas as pd
import re

wordw = pd.read_excel(pd.ExcelFile("F:/Data/Wordsworth Input.xlsx"),'Wordsworth Input')
score = pd.read_excel(pd.ExcelFile("F:/Data/Wordsworth Input.xlsx"),'Scrabble')  
score = score.set_index('Letter').T.to_dict('index')['Score']

wordw['not html'] = wordw['DownloadData'].apply(lambda x: bool(not re.search('[<>\=\(\)]',x)))
wordw['in poem'] = wordw['DownloadData'].apply(lambda x: bool(not re.search('(Composed|[Ww]ritten) in|^\s*$',x)))
wordw = wordw[wordw['not html'] & wordw['in poem']][['RowID','Poem','DownloadData']].copy()
wordw['Line #'] = wordw.sort_values(['RowID'], ascending=True).groupby(['Poem']).cumcount() + 1
wordw['Line'] = wordw['DownloadData'].apply(lambda x: re.sub('^[^\w]+','',x))

wordw['LineT'] = wordw['Line'].apply(lambda x: re.sub('[^\w\s]','',x.upper()).strip())

final = pd.concat([wordw[['Poem','Line #', 'Line']].reset_index(drop=True), 
                   pd.DataFrame([map(str.strip, x) for x in wordw['LineT'].str.split(' ').values.tolist()])], axis=1, sort=False)
final = final.melt(id_vars=['Poem','Line #', 'Line'], value_name='Word', var_name='Word #').dropna()
final['Word #'] = final['Word #']+1
final['Score'] = final['Word'].apply(lambda x: sum([score[c] for c in  list(x)]))
final['Max Score'] = final['Score'].groupby(final['Poem']).transform('max')
final['Highest Scoring Word?'] = (final['Score'] == final['Max Score'])
final = final.drop('Max Score', axis=1)
