import pandas as pd
import re

people_xlsx = pd.ExcelFile(r"C:\Data\PreppinData\PeopleData.xlsx")
data_xlsx = pd.ExcelFile(r"C:\Data\PreppinData\MetricData2021.xlsx")

location = pd.read_excel(people_xlsx,'Location').set_index('Location ID').T.to_dict('records')[0]

agent = pd.read_excel(people_xlsx,'People')
agent['Agent Name'] = agent['last_name'] + ', ' + agent['first_name']
agent['Location'] = agent['Location ID'].apply(lambda x: location[x])

leader = pd.read_excel(people_xlsx,'Leaders')
leader['Leader Name'] = leader['last_name'] + ', ' + leader['first_name']

agent = pd.merge(agent, leader[['id', 'Leader Name']].rename(columns={'id':'Leader 1'}), on='Leader 1')

date_dim = pd.read_excel(people_xlsx,'Date Dim')
date_dim['Year'] = date_dim['Month Start Date'].dt.year
date_dim['Month Start Date'] = date_dim['Month Start Date'].dt.date
date_dim = date_dim[date_dim['Year']==2021][['Month Start Date']]

correct_cols = {'AgentID':'id', 'Offered':'Calls Offered', 'Not Answered':'Calls Not Answered', 'Answered':'Calls Answered'}
temp = []
for sheet in data_xlsx.sheet_names:
    df = pd.read_excel(data_xlsx,sheet).rename(columns=correct_cols)
    df.insert(0,'Month Start Date',pd.to_datetime(f'2021-{sheet}-01', format='%Y-%b-%d'))
    temp.append(df)
call_data = pd.concat(temp)   
call_data['Month Start Date'] = call_data['Month Start Date'].dt.date

final = pd.merge(agent, date_dim, how='cross')
final = pd.merge(final, call_data, on=['id','Month Start Date'], how='left')  
goal = pd.read_excel(people_xlsx,'Goals')['Goals'].tolist()
for g in goal:
    final[g] = int(re.search('(\d+)$', g).group(1))
final['Not Answered Rate'] = round(final['Calls Not Answered']/final['Calls Offered'],3)
final['Agent Avg Duration'] = round(final['Total Duration']/final['Calls Answered'])
final['Met Not Answered Rate'] = (final['Not Answered Rate']*100 < final['Not Answered Percent < 5'])
final['Met Sentiment Goal'] = (final['Sentiment'] >= final['Sentiment Score >= 0'])

final = final[['id', 'Agent Name', 'Leader 1', 'Leader Name', 'Month Start Date','Location', 'Calls Answered', 'Calls Not Answered', 
               'Not Answered Rate', 'Met Not Answered Rate', 'Not Answered Percent < 5', 'Calls Offered', 'Total Duration', 
               'Agent Avg Duration', 'Transfers', 'Sentiment', 'Sentiment Score >= 0', 'Met Sentiment Goal']]
