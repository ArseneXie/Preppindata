import pandas as pd

games = pd.read_csv(r"C:\Data\PreppinData\Richard Osman's House of Games - Episode Guide - Players.csv")
games = games.rename(columns = {'Ser.':'Series', 'Wk.':'Week', 'F':'Fri_Score', 'Total':'Score',
                                'F.1':'Fri_Rank', 'Week':'Points', 'Week.1':'Original Rank'}).dropna(subset=['Series'])
games = games[~games['Series'].str.startswith('N')][['Series', 'Week', 'Player', 'Original Rank', 'Score', 'Points', 'Fri_Score', 'Fri_Rank']].copy()
games['Original Rank'] = games['Original Rank'].str.extract('(\d+)').astype(int)  
games['Fri_Rank'] = games['Fri_Rank'].str.extract('(\d+)').astype(int) 
games['Week'] = games['Week'].astype(int)

games['Points without double points Friday'] = games['Points'] - (5-games['Fri_Rank'])
games['Score if double score Friday'] = games['Score'] + games['Fri_Score']

games['Rank without double points Friday'] = games.groupby(['Week', 'Series'])['Points without double points Friday'].rank(method='min', ascending=False).astype(int)
games['Rank based on Score'] = games.groupby(['Week', 'Series'])['Score'].rank(method='min', ascending=False).astype(int)
games['Rank if Double Score Friday'] = games.groupby(['Week', 'Series'])['Score if double score Friday'].rank(method='min', ascending=False).astype(int)

games['Change in winner with no double points Friday?'] = games.apply(lambda x: x['Original Rank']==1 and x['Rank without double points Friday']>1, axis=1). \
                                                          groupby([games['Week'], games['Series']]).transform('max')
games['Change in winner based on Score?'] = games.apply(lambda x: x['Original Rank']==1 and x['Rank based on Score']>1, axis=1). \
                                            groupby([games['Week'], games['Series']]).transform('max')
games['Change in winner if Double Score Friday?'] = games.apply(lambda x: x['Original Rank']==1 and x['Rank if Double Score Friday']>1, axis=1). \
                                                    groupby([games['Week'], games['Series']]).transform('max')
games = games[['Series', 'Week', 'Player', 'Original Rank',
               'Rank without double points Friday', 'Change in winner with no double points Friday?',
               'Rank based on Score', 'Change in winner based on Score?',
               'Rank if Double Score Friday', 'Change in winner if Double Score Friday?',
               'Points', 'Score', 'Points without double points Friday', 'Score if double score Friday']]
games = games.sort_values(['Week', 'Series', 'Original Rank'])
