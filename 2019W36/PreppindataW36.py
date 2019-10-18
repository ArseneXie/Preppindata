import pandas as pd
import re

def convert_ht(df):
    df['ft'] = df['HT'].apply(lambda x: int(re.search(r"^(\d+)'",x).group(1)))
    df['inch'] = df['HT'].apply(lambda x: int(re.search(r'\s(\d+)"',x).group(1)))
    df['Height (m)'] = df.apply(lambda x: round((x['ft']*12+x['inch'])*2.54/100,2), axis=1)
    df.drop(['HT','ft','inch'], axis=1, inplace=True)
    
def convert_wt(df):
    df['Weight (KGs)'] = df['WT'].apply(lambda x: round(int(re.search(r'^(\d+)',x).group(1))*0.453592,2))
    df.drop(['WT'], axis=1, inplace=True)    
    
def jersey_no(df):
    df['NAME'] = df['NAME'].apply(lambda x: re.sub('(\d+)',',\\1',x))     
    temp = df['NAME'].str.split(',', n = 1, expand = True) 
    df['NAME'] = temp[0]
    df['Jersey Number'] = temp[1].astype('int')
    
def proc_all(df):
    convert_ht(df)
    convert_wt(df)
    jersey_no(df)
    
spurs = pd.read_csv("E:\PD - Week 36 - Data.csv")
nets = pd.read_csv("E:\PD - Week 36 - Brooklyn Data.csv")

proc_all(spurs)
proc_all(nets)
