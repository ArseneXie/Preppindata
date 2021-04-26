import pandas as pd
import re

df = pd.read_csv('F:\\Data\\PL Fixtures.csv').dropna()
big6=['Arsenal','Chelsea','Liverpool','Man Utd','Man City','Spurs']

def get_position(df):
    df['Home Score'] = df['Result'].apply(lambda x: int(re.search('^(\d+)',x).group(1)))
    df['Away Score'] = df['Result'].apply(lambda x: int(re.search('(\d+)$',x).group(1)))
    df['Home Goal Difference'] = df['Home Score'] - df['Away Score']
    df['Away Goal Difference'] = -1*df['Home Goal Difference']
    df['Home Point'] = df['Home Goal Difference'].apply(lambda x: 3 if x>0 else 1 if x==0 else 0)
    df['Away Point'] = df['Away Goal Difference'].apply(lambda x: 3 if x>0 else 1 if x==0 else 0)
    home = df[[c for c in df.columns if c[0:4]=='Home']].copy()
    home.columns = ['Team', 'Score', 'Goal Difference', 'Total Points']
    away = df[[c for c in df.columns if c[0:4]=='Away']].copy()
    away.columns = home.columns 
    
    final = pd.concat([home, away])
    final['Total Games Played'] = 1
    final = final.groupby('Team', as_index=False).agg({'Total Games Played':'sum', 'Total Points':'sum', 'Goal Difference':'sum'})
    final['Position'] = final[['Total Points', 'Goal Difference']].apply(tuple,axis=1).rank(method='dense',ascending=False).astype(int)
    return final[['Position', 'Team', 'Total Games Played', 'Total Points', 'Goal Difference']].copy()

finalA = get_position(df)

finalB = get_position(df[~(df['Home Team'].isin(big6) | df['Away Team'].isin(big6))].copy())
finalB = pd.merge(finalB, finalA[['Team','Position']].rename(columns={'Position':'Position Original'}), on='Team')
finalB['Position Change'] = finalB['Position Original'] - finalB['Position'] 
finalB = finalB[['Position Change', 'Position', 'Team', 'Total Games Played', 'Total Points', 'Goal Difference']]
