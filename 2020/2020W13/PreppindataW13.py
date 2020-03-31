import pandas as pd
import re
from datetime import datetime

xls = pd.ExcelFile("E:/Ticket Data.xlsx")
sla = pd.read_excel(xls,'SLA Agreements')
temp=[]
for sheet in [sh for sh in xls.sheet_names if re.match('^.{3}$',sh)]:
    df = pd.read_excel(xls,sheet)
    temp.append(df)
ticket = pd.concat(temp)   
ticket['Department'] = ticket['Ticket'].apply(lambda x: re.search('/(.*)/',x).group(1).strip())

ticket['MaxTimestamp'] = ticket['Timestamp'].groupby(ticket['Ticket']).transform('max')
ticket['CurrentTemp'] = ticket.apply(lambda x: x['Status Name'] if x['MaxTimestamp']==x['Timestamp'] else '', axis=1)
ticket['Current Status'] = ticket['CurrentTemp'].groupby(ticket['Ticket']).transform('max')

output1 = ticket[ticket['MaxTimestamp']==ticket['Timestamp']][['Ticket','Status Name']].copy()
output1 = output1.groupby('Status Name', as_index=False).agg({'Ticket':'count'})
output1 = output1.rename(columns={'Status Name':'Current Status','Ticket':'Ticket Count'})

ticket_sla = pd.merge(ticket[ticket['Status Name']=='Logged'],sla, how='inner', on='Department')[
    ['Ticket', 'Timestamp','Department', 'MaxTimestamp', 'Current Status', 'SLA Agreement']]
ticket_sla['OpenClose'] = ticket_sla['Current Status'].apply(lambda x: x if x=='Closed' else 'Open')
ticket_sla['bdfix'] = ticket_sla['Timestamp'].apply(lambda x: 1 if int(datetime.strftime(x,'%w'))==0 else 2 if int(datetime.strftime(x,'%w'))==6 else 0) 
ticket_sla['SLA Due'] = ticket_sla.apply(lambda x: x['Timestamp']+
                                         pd.tseries.offsets.BusinessDay(n = x['SLA Agreement']+x['bdfix']), axis=1)
ticket_sla['SLA Compare'] = ticket_sla.apply(lambda x: 'over' if x['MaxTimestamp'].date() > x['SLA Due'].date() else 'under', axis=1)

output2 = ticket_sla.groupby(['OpenClose','SLA Compare'], as_index=False).agg({'Ticket':'count'})
output2['Metric'] = output2['OpenClose'] + ' ' + output2['SLA Compare'] + ' SLA'
output2 = output2[(output2['Metric']=='Closed over SLA') | (output2['Metric']=='Open under SLA')]
output2 = output2.rename(columns={'Ticket':'Ticket Count'})
output2 = output2[['Metric','Ticket Count']]

output3 = ticket_sla[ticket_sla['OpenClose']=='Closed'].copy()
output3['Archieved'] = output3['SLA Compare'].apply(lambda x: 1 if x=='under' else 0)
output3 = output3.groupby('Department', as_index=False).agg({'Ticket':'count','Archieved':'sum'})
output3['Archieved %'] = output3['Archieved']/output3['Ticket']
output3['Rank'] = output3['Archieved %'].rank(method='dense',ascending=False).astype(int)
output3 = output3[['Rank','Archieved %','Department']].sort_values(by=['Rank'])
