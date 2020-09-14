import pandas as pd
import numpy as np
from datetime import date,datetime,timedelta
import re

def gen_datelist(sd, ed):
    return [d.date() for d in pd.date_range(sd, periods=(ed-sd).days+1).tolist()]

myhol = pd.read_excel(pd.ExcelFile("F:/Data/Start Date.xlsx"),'Holidays')  
twhol = pd.read_excel(pd.ExcelFile("F:/Data/Taiwan Holidays.xlsx"),sheet_name=0)  
start_date = date(2019,1,1)
to_date = date(2020,9,11)

twhol['Is Date'] = twhol['Date'].apply(lambda x: 'Y' if isinstance(x, datetime) else 'N')

twgolrg = twhol[twhol['Is Date']=='N'].copy()
twgolrg['From date'] = twgolrg.apply(lambda x: datetime.strptime(
    re.search('(.*)(?=\sto)',x['Date']).group(1)+' '+str(x['Year']),'%d %b %Y').date(), axis=1) 
twgolrg['To date'] = twgolrg.apply(lambda x: datetime.strptime(
    re.search('(?<=to\s)(.*)',x['Date']).group(1)+' '+str(x['Year']),'%d %b %Y').date(), axis=1) 

twhol = twhol[twhol['Is Date']=='Y'].copy()
twhol['Date'] = twhol.apply(lambda x: x['Date'].replace(year=x['Year']).date(), axis=1)

twhol_list = twhol['Date'].tolist()
for _,row in twgolrg.iterrows():
    twhol_list = twhol_list + gen_datelist(row['From date'], row['To date'])  
    
final = [start_date,to_date,
         np.busday_count(start_date+timedelta(days=1), to_date+timedelta(days=1), holidays=twhol_list)-myhol['Holidays'].sum()]    
final = pd.DataFrame(final).T 
final.columns=['Start Date', 'Today', 'Working Days']
