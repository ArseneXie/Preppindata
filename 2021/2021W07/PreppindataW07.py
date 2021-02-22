import pandas as pd

df = pd.read_excel(pd.ExcelFile("F:/Data/PGALPGAMoney2019.xlsx"),sheet_name=0)

df['Money per Event'] = df['MONEY']/df['EVENTS'] 
df['Tour Rank'] = df.groupby('TOUR')['MONEY'].rank(ascending=False).astype(int)
df['Overall Rank'] = df['MONEY'].rank(ascending=False).astype(int)
df['Difference of Ranking'] = df['Overall Rank'] - df['Tour Rank']

final = df.groupby(['TOUR'], as_index=False).agg({'Difference of Ranking':[('Avg Difference of Ranking', 'mean')], 
                                                  'Money per Event':[('Avg Money per Event', 'mean')],
                                                  'MONEY':[('Total Prize Money', 'sum')], 
                                                  'EVENTS':[('Number of Events' ,'sum')], 
                                                  'PLAYER NAME':[('Number of Players', 'nunique')]})
final.columns = [col[1] if col[1] else col[0] for col in final.columns.values]
final['Avg Money per Event'] = final['Avg Money per Event'].apply(lambda x: round(x))
final = pd.melt(final, id_vars='TOUR', var_name='Measure', value_name='Value')
final = final.pivot_table(index='Measure', columns='TOUR', values='Value', aggfunc=max).reset_index()
final['Difference between tours'] = final['LPGA'] - final['PGA'] 
