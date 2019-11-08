import pandas as pd
import re

xls = pd.ExcelFile("E:/PD Wk 39 .xlsx")

temp = []
for sheet in xls.sheet_names:
    df = pd.read_excel(xls,sheet)
    df.insert(0,'TimeType',re.search('^(\w+\s\w+)', sheet).group(1).strip())
    df.insert(0,'EntryType',re.sub('^(\w+\s\w+)','', sheet).strip())
    temp.append(df)
data = pd.concat(temp)   

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
