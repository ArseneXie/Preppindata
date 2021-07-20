import pandas as pd
import re

xlsx = pd.ExcelFile("F:/Data/InternationalPenalties.xlsx")
temp = []
for sheet in xlsx.sheet_names:
    df = pd.read_excel(xlsx,sheet)
    df.insert(0,'Source',sheet)
    df.columns = [x.title().strip() for x in df.columns]
    temp.append(df)
competition  = pd.concat(temp)[['Source', 'No.', 'Penalty Number', 'Winner', 'Loser', 'Winning Team Taker', 'Losing Team Taker']]

competition['Winner'] = competition['Winner'].str.strip()
competition['Loser'] = competition['Loser'].str.strip()
competition = competition.replace({'Winner':{'West Germany':'Germany'}, 'Loser':{'West Germany':'Germany'}})
competition['Winner Penalty Scored'] = competition['Winning Team Taker'].apply(lambda x: 1 if re.search('(scored)', str(x)) else 0)
competition['Winner Total Penalties'] = competition['Winning Team Taker'].apply(lambda x: 0 if pd.isna(x) else 1)
competition['Loser Penalty Scored'] = competition['Losing Team Taker'].apply(lambda x: 1 if re.search('(scored)', str(x)) else 0)
competition['Loser Total Penalties'] = competition['Losing Team Taker'].apply(lambda x: 0 if pd.isna(x) else 1)

finalA = competition[['Source', 'No.', 'Winner', 'Loser']].drop_duplicates().copy()
finalA = finalA.melt(id_vars=['Source', 'No.'],  value_name='Team', var_name='Win Lose')
finalA['Shootouts'] = finalA['Win Lose'].apply(lambda x: 1 if x=='Winner' else 0) 
finalA['Total Shootouts'] = 1
finalA = finalA.groupby(['Team'], as_index=False).agg({'Shootouts':'sum', 'Total Shootouts':'sum'})
finalA = finalA[finalA['Shootouts']>0]
finalA['Shootouts Win %'] = round(finalA['Shootouts']*100/finalA['Total Shootouts'])
finalA['Win % Rank'] = finalA['Shootouts Win %'].rank(method='dense', ascending=False).astype(int)
finalA = finalA[['Win % Rank', 'Shootouts Win %', 'Total Shootouts', 'Shootouts', 'Team']].sort_values(['Win % Rank', 'Shootouts'], ascending=[True, False])

finalB = competition[['Winner', 'Loser', 'Winner Penalty Scored', 'Winner Total Penalties', 'Loser Penalty Scored', 'Loser Total Penalties']].copy()
finalB = finalB.melt(id_vars=[c for c in finalB.columns if re.search('\s\w',c)],  value_name='Team', var_name='Win Lose')
finalB['Penalties Scored'] =  finalB.apply(lambda x: x['Winner Penalty Scored'] if x['Win Lose']=='Winner' else x['Loser Penalty Scored'], axis=1)
finalB['Total Penalties'] =  finalB.apply(lambda x: x['Winner Total Penalties'] if x['Win Lose']=='Winner' else x['Loser Total Penalties'], axis=1)
finalB = finalB.groupby(['Team'], as_index=False).agg({'Penalties Scored':'sum', 'Total Penalties':'sum'})
finalB['Penalties Missed'] = finalB['Total Penalties'] - finalB['Penalties Scored']
finalB['% Total Penalties Scored'] = round(finalB['Penalties Scored']*100/finalB['Total Penalties'])
finalB['Penalties Scored % Rank'] = finalB['% Total Penalties Scored'].rank(method='dense', ascending=False).astype(int)
finalB = finalB[['Penalties Scored % Rank', '% Total Penalties Scored', 'Penalties Missed', 'Penalties Scored', 'Team']].sort_values(['Penalties Scored % Rank', 'Penalties Scored'], ascending=[True, False])

finalC = competition[['Penalty Number', 'Winner Penalty Scored', 'Winner Total Penalties', 'Loser Penalty Scored', 'Loser Total Penalties']].copy()
finalC['Total Penalties'] = finalC['Winner Total Penalties'] + finalC['Loser Total Penalties'] 
finalC['Penalties Scored'] = finalC['Winner Penalty Scored'] + finalC['Loser Penalty Scored'] 
finalC = finalC.groupby(['Penalty Number'], as_index=False).agg({'Total Penalties':'sum', 'Penalties Scored':'sum'})
finalC['Penalties Missed'] = finalC['Total Penalties'] - finalC['Penalties Scored']
finalC['Penalties Scored %'] = round(finalC['Penalties Scored']*100/finalC['Total Penalties'])
finalC['Rank'] = finalC['Penalties Scored %'].rank(method='dense', ascending=False).astype(int)
finalC = finalC[['Rank', 'Penalties Scored %', 'Penalties Missed', 'Penalties Scored', 'Total Penalties', 'Penalty Number']].sort_values(['Rank', 'Penalty Number'], ascending=[True, True])