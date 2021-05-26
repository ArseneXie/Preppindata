import pandas as pd
import re

xlsx = pd.ExcelFile("F:/Data/PD 2021 Week 19 Input.xlsx")

lookup = {}
for sheet in [sh for sh in xlsx.sheet_names if re.match('.*Lookup Table$',sh)]:
    df = pd.read_excel(xlsx,sheet)
    col = df.columns[1]
    df.columns = ['Code', 'Name']
    df['Code'] = df['Code'].str.lower()
    lookup[col] = {k:v[0] for (k,v) in df.set_index('Code').T.to_dict('list').items()}

sched =  pd.read_excel(xlsx,'Project Schedule Updates')
sched['Week'] = sched['Week'].apply(lambda x: f'Week {x}')
sched['Commentary'] = sched['Commentary'].apply(lambda x: re.sub('(\s+)(?=\[)','@',x))
sched = pd.concat([sched['Week'], 
                   pd.DataFrame([map(str.strip, x) \
                                 for x in sched['Commentary'].str.split('@').values.tolist()])],
                  axis=1, sort=False)
sched = sched.melt(id_vars='Week', value_name='Commentary', var_name='ToDrop').drop('ToDrop', axis=1).dropna().reset_index(drop=True)
sched['Detail'] = sched['Commentary'].apply(lambda x: re.search('(?<=\]\s)(.*)',x).group(1))
sched['Days Noted'] = sched['Commentary'].apply(lambda x: int(re.search('(\d+)(?=\sday)',x).group(1)) if re.search('(\d+)(?=\sday)',x) else None)
for c in [('Name','(\w+)(?=\.$)'),('Project','(?<=\[)(\w+)'),('Sub-Project','(?<=/)(Mar|Op)'),('Task','(\w+)(?=\])')]:
    sched[c[0]] = sched['Commentary'].apply(lambda x: lookup[c[0]][(re.search(c[1],x).group(1)).lower()])
sched = sched[['Week', 'Project', 'Sub-Project', 'Task', 'Name', 'Days Noted', 'Detail']]    
