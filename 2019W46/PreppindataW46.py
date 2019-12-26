import pandas as pd
import re

xls = pd.ExcelFile("E:/2019 PD Wk 46.xlsx")
temp = []
for sheet in ['Nice List','Naughty List']:
    df = pd.read_excel(xls,sheet)
    df.insert(0,'List',sheet)
    temp.append(df)
all_list = pd.concat(temp).rename(columns={'Name':'Name Part'})   
all_list['key'] = 1
present = pd.read_excel(xls,'Present List').rename(columns={'Address':'Address Part'})
present['key'] = 1
join_list = pd.merge(all_list,present,on='key')
join_list['key'] = join_list.apply(lambda x: 
                                     1 if re.search(x['Name Part'],x['Name']) and re.search(x['Address Part'],x['Address']) else 0, axis=1)
    
detail_list = join_list.query('`key`==1')    
detail_list = detail_list.groupby(['List','Name','Address','Family Role','Item'], as_index=False).agg({'Elves Build Time (min)':'max',
                                                                                                       'Reason':'min'})    

summary =  detail_list.groupby(['List'], as_index=False).agg({'Elves Build Time (min)':'sum'})
summary['Total Hours Build Time'] = round(summary['Elves Build Time (min)']/60)
summary.drop('Elves Build Time (min)', axis=1, inplace=True)

missing_list = pd.merge(present,join_list.query('`key`==1'), how='left', 
                        on=['Name','Address Part','Family Role'],suffixes = ['','_y'], indicator='Check')
missing_list = missing_list.query("`Check`=='left_only'")[['Name', 'Address Part', 'Item', 'Family Role','Elves Build Time (min)']]