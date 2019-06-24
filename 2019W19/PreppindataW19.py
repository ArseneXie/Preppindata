import pandas as pd
import re

xls = pd.ExcelFile(r"E:\2018 Tour de France times.xlsx")
record = pd.read_excel(xls,"Sheet1") 

def get_secs(timestr):
    timepart = (re.findall('\d+',timestr)) + ['00']
    return sum([int(int(v)*pow(60,i-1)) for i,v in enumerate(timepart[::-1]) ])

record['Gap in Sec'] = record.apply(lambda x: get_secs(x['Gap']),axis=1)   
final = record.groupby('Team',as_index=False).agg({'Gap in Sec':'mean', 'Rider':'count'})
final = final[(final['Rider']>=7) & (final['Gap in Sec']<=60*100)] 
final['Team Avg Gap in Min'] = final.apply(lambda x: int(x['Gap in Sec']/60),axis=1)   
final.drop(['Gap in Sec'],axis=1,inplace = True)
final.rename(columns = {'Rider':'Number of Riders'}, inplace = True)

