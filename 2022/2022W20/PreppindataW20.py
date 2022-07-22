import pandas as pd
import re

xlsx = pd.ExcelFile(r"C:\Data\PreppinData\TC22 Input.xlsx")

regs = pd.read_excel(xlsx, 'Registrations')
regs['Online/In Person'] = regs['Online/In Person'].str.replace('^O.*','Online',regex=True)
regs['Online/In Person'] = regs['Online/In Person'].str.replace('^I.*','In Person',regex=True)

regs['Company'] = regs['Email'].apply(lambda x: re.search('(?<=@)([^\.]+)', x).group(1))
regs['Planning to attend'] = regs['Session ID'].groupby(regs['Email']).transform('nunique') 
regs = regs.merge(pd.read_excel(xlsx, 'Sessions'), on='Session ID')

not_att = regs.merge(pd.read_excel(xlsx, 'In Person Attendees'), 
                     on=['Session', 'First Name', 'Last Name'], 
                     how = 'outer', indicator = True).query('_merge == "left_only"').drop('_merge', axis=1)
not_att = not_att.merge(pd.read_excel(xlsx, 'Online Attendees'), 
                        on=['Session', 'Email'], 
                        how = 'outer', indicator = True).query('_merge == "left_only"')

not_att['Not attended'] = not_att['Session ID'].groupby(regs['Email']).transform('nunique') 
not_att['Not Attended %'] = not_att['Not attended']/not_att['Planning to attend']*100
not_att = not_att.rename(columns={'Session':'Session not attended'})

not_att = not_att[['Company', 'First Name', 'Last Name', 'Email', 'Online/In Person', 'Session not attended', 'Not Attended %']]
