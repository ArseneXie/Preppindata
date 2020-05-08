import pandas as pd
import re

game_time = 90

data = pd.read_excel(pd.ExcelFile("E:/Liverpool Lineups.xlsx"),sheet_name=0, skiprows=4, header=[1,2]).dropna(axis=1, how='all')
data.columns = [col[1] if re.match('^sub', str(col[1])) else col[0]+' '+str(col[1]) for col in data.columns.values]

player = data[[col for col in data.columns.values if re.match('^(Match Details No|Start|Subst)', col)]].copy()
player = player.melt(id_vars='Match Details No.',value_name='Player Name', var_name='Type Number')
player['Start Appearance'] = player['Type Number'].apply(lambda x: 1 if re.match('^Start', x) else 0)
player['Player No'] = player['Type Number'].apply(lambda x: int(re.search('(\d+)$', x).group(1)))

submap = data[[col for col in data.columns.values if re.match('^(Match Details No|sub)', col)]].copy()
submap = submap.melt(id_vars='Match Details No.',value_name='Value', var_name='Type').dropna()
submap['Value'] = submap['Value'].astype(int)
submap['subX'] = submap['Type'].apply(lambda x: re.search('^(sub\d)', x).group(1))
submap['ValueType'] = submap['Type'].apply(lambda x: 'SubOn' if re.search('\.[1]$', x) else 'SubMins' if re.search('\.[12]$', x) else 'SubOff')
submap = submap.pivot_table(index=['Match Details No.','subX'], columns='ValueType', values='Value', aggfunc=max).reset_index()
submap = submap.melt(id_vars=['Match Details No.','subX','SubMins'],value_name='Player No', var_name='OnOff')
submap['Mins Played'] = submap.apply(lambda x: x['SubMins'] if x['OnOff']=='SubOff' else game_time-x['SubMins'], axis=1)

final = pd.merge(player,submap,on=['Match Details No.','Player No'], how='left')
final['Appearances'] = final.apply(lambda x: 1 if x['OnOff']=='SubOn' else x['Start Appearance'], axis=1)
final['Mins Played'].fillna(final['Start Appearance']*game_time, inplace=True)
final = final.groupby(['Player Name'], as_index=False).agg({'Match Details No.':'nunique',
                                                            'Appearances':'sum','Mins Played':'sum'}).rename(columns={'Match Details No.':'In Squad'})
final['Mins Played'] = final['Mins Played'].astype(int)
final['Mins per Game'] = final.apply(lambda x: 0 if x['Appearances']==0 else x['Mins Played']/x['Appearances'], axis=1)
