import pandas as pd
import re

def clean_country(x):
    return 'England' if re.search('(gland)',x,re.IGNORECASE) else \
        'Scotland' if re.search('(^sc)',x,re.IGNORECASE) else \
            'Netherlands' if re.search('(Netherland)',x,re.IGNORECASE) else \
                'United States' if re.search('(United)',x,re.IGNORECASE) else x
def date_ymd_str(x):
    x = re.sub('\D','@', re.sub('(^.*)(?:Dec)(.*$)',r'\1/12/\2', re.sub('(^.*)(?:Jan)(.*$)',r'\1/01/\2', re.sub('\s','', re.sub('(.*\D$)',r'\1 2020',x)))))
    return re.sub('(?:@*)(\d+)(?:@*)(\d+)(?:@*)(\d+)',r'\3/\2/\1',x) if re.search('(@*\d+@*((0?[1-9])|(1[0-2]))@*\d{4})',x) else \
        re.sub('(?:@*)(\d+)(?:@*)(\d+)(?:@*)(\d+)',r'\3/\1/\2',x) if re.search('(@*((0?[1-9])|(1[0-2]))@*\d+@*\d{4})',x) else \
            re.sub('(?:@*)(\d+)(?:@*)(\d+)(?:@*)(\d+)',r'\1/\2/\3',x) if re.search('(@*\d{4}@*((0?[1-9])|(1[0-2]))@*\d+)',x) else x
def time_str(x):
    dx = re.sub('\D','',x)
    return str(int(re.search('(\d+)(?=\d{2})',dx).group(1))+(12 if re.search('(p|P)',x) else 0)).zfill(2)+':'+re.search('(\d{2}$)',dx).group(1)
          
result = pd.read_csv(r'E:/PD 2020 Wk 4 Input.csv' )
question = pd.read_csv(r'E:/Store Survey Results - Question Sheet.csv' )

result['Id'] = result.groupby('Question Number').cumcount()+1
result = pd.merge(result,question,how='inner',left_on='Question Number',right_on='Number')
result.drop(['Question Number','Number',],axis=1,inplace=True)
result['Country'] = result.apply(lambda x: x['Country'] if x['Country'] else x['Store'], axis=1)
result['Country'] = result['Country'].apply(lambda x: clean_country(x))
result['DoB'].fillna('',inplace=True)

final = result.pivot_table(index=[c for c in result.columns if not re.match('Question|Answer',c)],
                           columns='Question',values='Answer',aggfunc=max).reset_index()
final['Date'] = final['What day did you fill the survey in?'].apply(lambda x: date_ymd_str(x))
final['Time'] = final['What time did you fill the survey in?'].apply(lambda x: time_str(x))
final['Completion Date'] = final.apply(lambda x: 
                                       pd.to_datetime(x['Date'] + ' ' + ('00:00' if x['Time']=='24:00' else x['Time']), format='%Y/%m/%d %H:%M')
                                       + pd.DateOffset(days=(1 if x['Time']=='24:00' else 0)),axis=1)
final['Age of Customer'] = final['DoB'].apply(lambda x: 2020-int(re.search('(\d+$)',x).group(1)) if re.search('(\d+$)',x) else None)    
final['OrderAsc'] = final.groupby(['Country','Store','Name'])['Completion Date'].rank().astype(int)
final['OrderDesc'] = final.groupby(['Country','Store','Name'])['Completion Date'].rank(ascending=False).astype(int)
final['Would you recommend C&BSco to your friends and family? (Score 0-10)']=final['Would you recommend C&BSco to your friends and family? (Score 0-10)'].astype(int)
final['Result'] = final.apply(lambda x: 'First' if x['OrderAsc']==1 else 'Latest' if x['OrderDesc']==1 else 'Drop', axis=1)
final['Detractor'] = final['Would you recommend C&BSco to your friends and family? (Score 0-10)'].apply(lambda x: 1 if x<=6 else None)
final['Promoter'] = final['Would you recommend C&BSco to your friends and family? (Score 0-10)'].apply(lambda x: 1 if x>=9 else None)
final['Passive'] = final['Would you recommend C&BSco to your friends and family? (Score 0-10)'].apply(lambda x: 1 if 6<x<9 else None)
final = final.query("Result!='Drop'")[['Country', 'Store', 'Name','Completion Date','Result',
                                        'Would you recommend C&BSco to your friends and family? (Score 0-10)',
                                        'Promoter','Detractor','Passive',
                                        'Age of Customer','If you would, why?',"If you wouldn't, why?"]].copy()



