import pandas as pd
import re

xlsx = pd.ExcelFile("F:/Data/NBA 2018_19 Results.xlsx")

temp = []
for sheet in xlsx.sheet_names:
    df = pd.read_excel(xlsx,sheet)
    temp.append(df)
game = pd.concat(temp)[[c for c in df.columns if re.match('Date|.*Neutral|PTS.*',c)]] 
game.columns = ['Date', 'Visitor', 'Visitor PTS', 'Home', 'Home PTS']
final = game.melt(id_vars= ['Date','Visitor PTS','Home PTS'], var_name='Type', value_name='Team')
final['Win'] = final.apply(lambda x: 1 if x[x['Type']+' PTS']==max(x['Visitor PTS'],x['Home PTS']) else 0,axis=1)
final['Game Number per Team'] = final.groupby(['Team'])['Date'].rank().astype(int)
final['Win'] = final.sort_values('Date').groupby(['Team'])['Win'].cumsum()
final['Rank'] = final.sort_values(['Win','Team'], ascending=[False,True]).groupby('Game Number per Team').cumcount()+1
final = final[['Rank','Win','Team', 'Game Number per Team']].copy()
