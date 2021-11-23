import pandas as pd
import re

xlsx = pd.ExcelFile(r"C:\Data\PreppinData\TC Input.xlsx")
final_cols = ['Subject', 'Attendee', 'Contact Type', 'Contact']
lookup = pd.read_excel(xlsx, 'Attendees')
temp = []
for sheet in [sh for sh in xlsx.sheet_names if re.match('.*Nov',sh)]:
    df = pd.read_excel(xlsx,sheet)
    df.insert(0,'Date',re.sub('(\d+)(?:\w+\s+)(\w+)','2021-\\2-\\1',sheet))
    temp.append(df)
meeting = pd.concat(temp)   
meeting['Time'] = meeting['Session Time'].apply(lambda x: re.search('(\d+:\d+)',f'{x}:00').group(1)) 
meeting['DateTime'] = meeting.apply(lambda x: pd.to_datetime(x['Date']+' '+x['Time'], format='%Y-%b-%d %H:%M'), axis=1)
meeting = meeting.reset_index()[['Session ID', 'DateTime', 'Subject','Attendee IDs']].copy()
meeting = pd.concat([meeting[['Session ID', 'DateTime', 'Subject']], 
                   pd.DataFrame([map(int, x) \
                                 for x in meeting['Attendee IDs'].str.split(',').values.tolist()])], axis=1, sort=False)
meeting = meeting.melt(id_vars=['Session ID', 'DateTime', 'Subject'],
                       value_name='Attendee ID', var_name='ToDrop').drop('ToDrop', axis=1).dropna().reset_index(drop=True)

meeting = meeting.merge(lookup, on='Attendee ID').drop('Attendee ID', axis=1)

direct = meeting.merge(meeting[['Session ID', 'Attendee']].rename(columns={'Attendee':'Contact'}), on='Session ID')
direct = direct[direct['Attendee'] != direct['Contact']].copy()
direct['Contact Type'] = 'Direct Contact'

indirect = pd.merge(direct.rename(columns={'Contact':'Direct Contact'}),
                    direct[['DateTime', 'Subject', 'Attendee', 'Contact']]\
                        .rename(columns={'Attendee':'Direct Contact', 'DateTime':'Previous DateTime'}),
                        on=['Subject','Direct Contact'])
indirect = indirect.query('`DateTime`>`Previous DateTime`')
indirect = indirect[indirect['Attendee'] != indirect['Contact']].copy()
indirect['Contact Type'] = 'Indirect Contact'

final = pd.concat([direct[final_cols], indirect[final_cols]])
final['Type Index'] = final.groupby(['Subject', 'Attendee','Contact'])['Contact Type'].rank(method='first', ascending=True).astype(int)
final = final[final['Type Index']==1].drop('Type Index', axis=1)
