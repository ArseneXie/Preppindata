import pandas as pd
import re

game_time = 90

data = pd.read_excel(pd.ExcelFile("E:/Liverpool Lineups.xlsx"),sheet_name=0, skiprows=4, header=[1,2]).dropna(axis=1, how='all')
data.columns = [col[1] if re.match('^sub', str(col[1])) else col[0]+' '+str(col[1]) for col in data.columns.values]

player = data[[col for col in data.columns.values if re.match('^(Match Details No|Match Details Formation|Start|Subst)', col)]].copy()
player = player.melt(id_vars=['Match Details No.','Match Details Formation'],value_name='Player Name', var_name='Type Number')
player['Start Appearance'] = player['Type Number'].apply(lambda x: 1 if re.match('^Start', x) else 0)
player['Player No'] = player['Type Number'].apply(lambda x: int(re.search('(\d+)$', x).group(1)))

submap = data[[col for col in data.columns.values if re.match('^(Match Details No|sub)', col)]].copy()
submap = submap.melt(id_vars='Match Details No.',value_name='Value', var_name='Type').dropna()
submap['Value'] = submap['Value'].astype(int)
submap['subX'] = submap['Type'].apply(lambda x: re.search('^(sub\d)', x).group(1))
submap['ValueType'] = submap['Type'].apply(lambda x: 'SubOn' if re.search('\.[1]$', x) else 'SubMins' if re.search('\.[12]$', x) else 'SubOff')
submap['SubOffPos'] = submap.apply(lambda x: x['Value'] if x['ValueType']=='SubOff' else 0, axis=1)
submap['SubOff Position'] = submap['SubOffPos'].groupby([submap['Match Details No.'],submap['subX']]).transform('sum')
submap = submap.pivot_table(index=['Match Details No.','subX','SubOff Position'], columns='ValueType', values='Value', aggfunc=max).reset_index()
submap = submap.melt(id_vars=['Match Details No.','subX','SubOff Position','SubMins'],value_name='Player No', var_name='OnOff')
submap['Mins Played'] = submap.apply(lambda x: x['SubMins'] if x['OnOff']=='SubOff' else game_time-x['SubMins'], axis=1)

output1 = data[['Match Details Location','Match Details Result', 'Match Details Formation','Match Details Oppo Form.']].copy()
temp = output1['Match Details Result'].str.split('-', n = 1, expand = True) 
output1['GoalsA'] = temp[0].astype('int64') 
output1['GoalsB'] = temp[1].astype('int64')
output1['Liverpool Goals'] = output1.apply(lambda x: x['GoalsA'] if x['Match Details Location']=='H' else x['GoalsB'], axis=1)
output1['Opposition Goals'] = output1.apply(lambda x: x['GoalsA'] if x['Match Details Location']=='A' else x['GoalsB'], axis=1)
output1 = output1.rename(columns={'Match Details Formation':'Formation','Match Details Oppo Form.':'Oppo Form.'})
output1 = output1.groupby(['Formation','Oppo Form.'],as_index=False).agg({'Liverpool Goals':[('Games Played','count'),('Liverpool Goals', 'sum'), ('Avg Goals Scored', 'mean')],
                                                                          'Opposition Goals':[('Opposition Goals', 'sum'), ('Avg Goals Conceded', 'mean')]})
output1.columns = [col[1] if col[1] else col[0] for col in output1.columns.values]

plist = pd.read_excel(pd.ExcelFile("E:/PlayerList.xlsx"),sheet_name=0)
plist['Preferred Position'] = plist['Player Name'].apply(lambda x: re.search('([A-Z])(?=\))',x).group(1))
plist['Player Name'] = plist['Player Name'].apply(lambda x: re.search('(\D+)(?=\()',x).group(1).strip())
plist['Last Name'] = plist['Player Name'].apply(lambda x: re.sub('^\S+\s','',x).lower())

position = pd.read_excel(pd.ExcelFile("E:/Formation Positions.xlsx"),sheet_name=0)

output2 = pd.merge(player,submap,on=['Match Details No.','Player No'], how='left').rename(columns={'Match Details Formation':'Formation Name'})
output2['Appearances'] = output2.apply(lambda x: 1 if x['OnOff']=='SubOn' else x['Start Appearance'], axis=1)
output2['Mins Played'].fillna(output2['Start Appearance']*game_time, inplace=True)
output2['Last Name'] = output2['Player Name'].str.lower()
output2 = pd.merge(output2.drop('Player Name', axis=1),plist,on='Last Name')
output2['Player Position'] = output2.apply(lambda x: x['Player No'] if pd.isna(x['SubOff Position']) else x['SubOff Position'], axis=1)
output2 = pd.merge(output2,position,on=['Player Position','Formation Name'])
output2 = output2.groupby(
    ['Player Name','Position Type','Position Name','Preferred Position'],as_index=False).agg({'Appearances':'sum','Mins Played':'sum'})
output2 = output2[output2['Appearances']>0].copy()
output2['oop'] = output2.apply(lambda x: 0 if x['Position Type'][0:1]==x['Preferred Position'] else x['Appearances'], axis=1)
output2['Games Oop'] = output2['oop'].groupby(output2['Player Name']).transform('sum')
output2 = output2.rename(columns={'Appearances':'No Times Played'}).drop(['Preferred Position','oop'],axis=1).copy()