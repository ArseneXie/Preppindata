import pandas as pd
import re
from datetime import datetime

xls = pd.ExcelFile("E:/PD - NBA Results.xlsx")
team_list = pd.read_excel(xls,"Team List").set_index('Team').T.to_dict('dict')
def get_conf(tname):
    return team_list[tname]['Conference']

temp = []
for sheet in [sh for sh in xls.sheet_names if re.search('Results$',sh)]:
    df = pd.read_excel(xls,sheet)
    temp.append(df.rename(columns={df.columns[5]:'PTS_H'}))
games = pd.concat(temp)[['Date','Visitor/Neutral','PTS','Home/Neutral','PTS_H']].dropna().copy()
games['Date'] =  games['Date'].apply(lambda x: datetime.strptime(re.sub('^\w+\s','',x),'%b %d %Y'))
games['Away Conf'] = games['Visitor/Neutral'].apply(lambda x: get_conf(x))
games['Home Conf'] = games['Home/Neutral'].apply(lambda x: get_conf(x))
games['In Conf'] = games.apply(lambda x: x['Away Conf']==x['Home Conf'], axis=1)
games['Away'] =  games.apply(lambda x: [x['Away Conf'],x['Visitor/Neutral'],('W' if x['PTS']>x['PTS_H'] else 'L')], axis=1)
games['Home'] =  games.apply(lambda x: [x['Home Conf'],x['Home/Neutral'],('W' if x['PTS_H']>x['PTS'] else 'L')], axis=1)
games = games[['Date','In Conf','Away','Home']].copy()

games = games.melt(id_vars=['Date','In Conf'],value_name='Team data', var_name='Away Home')
games['Conference'] = games['Team data'].apply(lambda x: x[0])
games['Team'] = games['Team data'].apply(lambda x: x[1])
games['Win Lose'] = games['Team data'].apply(lambda x: x[2])
games['Last N'] = games.groupby('Team')['Date'].rank(ascending=False).astype(int)


wl_team = games.groupby(['Conference','Team','Win Lose']).agg({'Date':'count'}).rename(columns={'Date':'Value'})
wl_aorh

final = pd.concat([games.groupby(['Conference','Team','Win Lose']).agg({'Date':'count'}).rename(columns={'Date':'Game Count'})
    ])


final = ((games.groupby(['Conference','Team','Win Lose']).agg({'Date':'count'}).rename(columns={'Date':'Team Level'})).join(
    games.groupby(['Conference','Team','Win Lose','Away Home']).agg({'Date':'count'})).reset_index())

games['Away C']

data['Pageviews %'] = data['Pageviews'].apply(lambda x: re.search('(?<=\()(.*)(?=%)', str(x)).group(1).replace('<1','0.5') \
    if re.search('(?<=\()(.*)(?=%)', str(x)) else None)
data['Pageviews Value'] = data['Pageviews'].apply(lambda x: int(re.search('^(\d+)', str(x)).group(1).strip()))       
data['Pageviews % Missing'] = data['Pageviews Value']/data.groupby(['EntryType','TimeType'])['Pageviews Value'].transform('sum')*100
data['Pageviews %'] = data.apply(lambda x: x['Pageviews %'] if x['Pageviews %'] else str(int(x['Pageviews % Missing'])), axis=1)
data.drop(['Pageviews % Missing','Pageviews'], inplace= True, axis=1)

data = data.melt(id_vars=[c for c in data.columns if not re.match('^Pageviews',c)],
                          value_name='R2C Value', var_name='Val Type')
data['R2C Value']=data['R2C Value'].astype('float')
data['R2C Col'] = data['TimeType']+' '+data['Val Type']
data.drop(['TimeType','Val Type'], inplace= True, axis=1)
final = data.pivot_table(index=['EntryType','Entry'],
                                columns='R2C Col', values='R2C Value', aggfunc=max).reset_index()
final['Change in % This Month'] = final['This Month Pageviews %']-final['All Time Pageviews %'] 
final = final.sort_values(by=['This Month Pageviews Value'],ascending=False)

browser_output = final.query("EntryType=='Browsers'").drop('EntryType', axis=1)
origin_output = final.query("EntryType=='Origin'").drop('EntryType', axis=1)
os_output = final.query("EntryType=='Operating System'").drop('EntryType', axis=1)
