import pandas as pd
import re
from dateutil.relativedelta import relativedelta

xls = pd.ExcelFile("E:\PD - ESPN stats.xlsx")

def clean_WL(wl):
    if wl[0:5]=='2019-':
        wl = re.search('\d+-\d+\s', wl).group(0).strip()
        wl = '-'.join(s.lstrip('0') for s in wl.split('-')[::-1])
    else:
        wl
    return wl    

espn = pd.read_excel(xls,"Sheet1",converters={'W-L':str}) 
espn['W-L'] = espn.apply(lambda x: clean_WL(x['W-L']),axis=1) 


for cols in ['HI POINTS','HI REBOUNDS','HI ASSISTS']:
    temp = espn[cols].str.split(' ', n = 1, expand = True) 
    espn[cols+' - Player'] = temp[0]
    espn[cols+' - Value'] = temp[1].astype('int64')
    
""" 
#  Alternative solution for HI POINTS,HI REBOUNDS,HI ASSISTS:
    
espn = pd.melt(espn, id_vars=['DATE', 'OPPONENT','RESULT','W-L'], 
                 var_name='VARA', value_name='TEMPA')
temp = espn['TEMPA'].str.split(' ', n = 1, expand = True) 
espn['Player'] = temp[0] 
espn['Value'] = temp[1].astype('int64') 
espn.drop('TEMPA',axis=1,inplace = True)
espn = espn.pivot_table(index = ['DATE', 'OPPONENT','RESULT','W-L'],
                          columns='VARA',
                          values=['Player','Value'],
                          aggfunc={"Player":'max',"Value":'max'})

espn.columns=[' - '.join(str(s).strip() for s in col[::-1] if s) for col in espn.columns]
espn.reset_index(inplace = True)
""" 
    
espn['True Date'] = espn.apply(lambda x: x['DATE'] if x['DATE'].month<10 else x['DATE'] + relativedelta(years=-1),axis=1) 
espn['OPPONENT(clean)'] = espn.apply(lambda x: re.sub(r'^(@|vs)', '',x['OPPONENT']),axis=1) 
espn['Win or Loss'] = espn.apply(lambda x: x['RESULT'][0:1],axis=1)     
espn['Home or Away'] = espn.apply(lambda x: 'Away' if x['OPPONENT'][0:1]=='@' else 'Home',axis=1)     

final = espn[['OPPONENT(clean)','HI ASSISTS - Player','HI ASSISTS - Value','HI REBOUNDS - Player','HI REBOUNDS - Value', \
              'HI POINTS - Player','HI POINTS - Value','Win or Loss','Home or Away','True Date','OPPONENT','RESULT','W-L']]