import pandas as pd
import re
import datetime as dt

xlsx = pd.ExcelFile("F:/Data/Prep Tips live chat logs.xlsx")
GMT_offset = {'APAC':-11,'EMEA':-1,'AM':5}

temp = []
for sheet in xlsx.sheet_names:
    df = pd.read_excel(xlsx,sheet)
    df.insert(0,'Location',re.search('^(\w+)', sheet).group(1).strip())
    temp.append(df)
data = pd.concat(temp)   

data['Date (GMT)'] = data.apply(lambda x: dt.datetime.combine(dt.date(2020, 10, 7),x['Time'])+dt.timedelta(hours = GMT_offset[x['Location']]), axis=1)
data['Seq'] = data.sort_values(['Date (GMT)'], ascending=True).groupby(['Location','Who']).cumcount() + 1
data = data[~((data['Who']=='Carl Allchin') & (data['Seq']==1))].copy()
data['Category'] = data.apply(lambda x: 'Intro' if x['Seq']==1 else 'Question' if re.search('\?$',x['Comment']) else 'Answer', axis=1)

output1 = data[(data['Category']=='Intro')][['Date (GMT)', 'Location', 'Who', 'Comment']].copy()
output1['City'] = output1['Comment'].apply(lambda x: re.search('^([\w\s]+)',x).group(1))
output1['Country'] = output1.apply(lambda x: 'United States' if x['Location']=='AM' else re.search(',([\w\s]+)',x['Comment']).group(1).strip(), axis=1)
output1['First Time Indicator?'] = output1['Comment'].apply(lambda x: 1 if re.search('(first time)',x.lower()) else 0)
output1 = output1[['Date (GMT)', 'Location', 'City', 'First Time Indicator?', 'Country', 'Who']]

output2 = data[~(data['Category']=='Intro')].copy()
output2 = output2.groupby(['Location','Category'], as_index=False).agg({'Who':'count'})
output2 = output2.rename(columns={'Category':'Question or Answer','Who':'Instances'})
