import pandas as pd
import re
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

xlsx = pd.ExcelFile(r"E:\PD Week 28 Input.xlsx")
sheet_name = xlsx.sheet_names[0]
data = pd.read_excel(xlsx,sheet_name,header=[0, 1]) 
data.columns = [col[0] if re.match('^Unnamed',col[1]) else col[0]+'-'+col[1] for col in data.columns.values]
data['Accum Length (mins)']=data.sort_values('Observation Interval').groupby(['Employee'])['Observation Length (mins)'].cumsum()
data['Observation Start Time']=data.apply(lambda x: dt.strptime(re.search('((\d+\.*)+)',sheet_name).group(0)+' '+str(x['Observation Start Time']),
    '%d.%m.%Y %H:%M:%S')+relativedelta(minutes=x['Accum Length (mins)']-x['Observation Length (mins)']),axis=1) 
data.drop('Accum Length (mins)',axis=1,inplace = True)
data = data.melt(id_vars=[c for c in data.columns if not re.match('(.*-.*)',c)],
                          value_name='Type Value', var_name='Type Name').dropna().drop('Type Value',axis=1)
temp = data['Type Name'].str.split('-',n = 1, expand = True)
data['Real Col Name'] = temp[0].apply(lambda x: re.sub('\sWith$','',x))
data['Real Col Value'] = temp[1]
data.drop('Type Name',axis=1,inplace = True)
final = data.pivot_table(index=[c for c in data.columns if not re.match('^Real',c)],
                                columns='Real Col Name', values='Real Col Value', aggfunc=max)
final.reset_index(inplace=True)
