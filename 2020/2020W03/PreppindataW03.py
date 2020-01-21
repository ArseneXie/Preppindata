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
games['Away check'] = games['Away Home'].apply(lambda x: 1 if x=='Away' else 0)
games['Home check'] = games['Away Home'].apply(lambda x: 1 if x=='Home' else 0)
games['Last N'] = games.groupby('Team')['Date'].rank(ascending=False).astype(int)
games['L10 check'] = games['Last N'].apply(lambda x: 1 if x<=10 else 0)
games['Conf check'] = games['In Conf'].apply(lambda x: 1 if x else 0)

wl_team = games.groupby(['Conference','Team','Win Lose'],as_index=False).agg({'Date':'count'}).rename(columns={'Date':'Value'})
wl_away = games.groupby(['Conference','Team','Win Lose'],as_index=False).agg({'Away check':'sum'}).rename(columns={'Away check':'Value'})
wl_away['Win Lose'] = wl_away['Win Lose'].apply(lambda x: 'Away '+x)
wl_home = games.groupby(['Conference','Team','Win Lose'],as_index=False).agg({'Home check':'sum'}).rename(columns={'Home check':'Value'})
wl_home['Win Lose'] = wl_home['Win Lose'].apply(lambda x: 'Home '+x)
wl_last = games.groupby(['Conference','Team','Win Lose'],as_index=False).agg({'L10 check':'sum'}).rename(columns={'L10 check':'Value'})
wl_last['Win Lose'] = wl_last['Win Lose'].apply(lambda x: 'L10 '+x)
wl_conf = games.groupby(['Conference','Team','Win Lose'],as_index=False).agg({'Conf check':'sum'}).rename(columns={'Conf check':'Value'})
wl_conf['Win Lose'] = wl_conf['Win Lose'].apply(lambda x: 'Conf '+x)
wl_strk = games.groupby(['Conference','Team','Win Lose'],as_index=False).agg({'Last N':'min'}).rename(columns={'Last N':'Value'})
wl_strk['Win Lose'] = wl_strk['Win Lose'].apply(lambda x: 'Strk '+x)

final = pd.concat([wl_team, wl_conf,  wl_home, wl_away, wl_last, wl_strk], sort=False, ignore_index=True)
final = final.pivot_table(index=['Conference','Team'], columns='Win Lose', values='Value', aggfunc=max).reset_index()
for cate in ['Conf','Home','Away','L10']:
    final[cate] = final.apply(lambda x: str(x[cate+' W'])+'-'+str(x[cate+' L']), axis=1)
final['Pct'] = round(final['W']/(final['L']+final['W']),3)
final['Strk'] = final.apply(lambda x: 'W'+str(x['Strk L']-1) if x['Strk W']==1 else 'L'+str(x['Strk W']-1), axis=1)
final['Rank'] = final.groupby('Conference')['Pct'].rank(ascending=False,method='max').astype(int)
final_east = final.query("Conference=='Eastern'")[['Rank','Team','W','L','Pct','Conf','Home','Away','L10','Strk']].sort_values(by='Rank')
final_west = final.query("Conference=='Western'")[['Rank','Team','W','L','Pct','Conf','Home','Away','L10','Strk']].sort_values(by='Rank') 
