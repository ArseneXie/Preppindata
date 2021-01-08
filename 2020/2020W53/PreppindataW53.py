import pandas as pd
import re
from datetime import datetime

old_star = pd.concat([pd.read_csv(r"F:\Data\Old Star Signs.csv", header=None, usecols=[0,1], names=['Old Star Sign', 'DateRange']),
                      pd.read_csv(r"F:\Data\Old Star Signs.csv", header=None, usecols=[2,3], names=['Old Star Sign', 'DateRange']),
                      pd.read_csv(r"F:\Data\Old Star Signs.csv", header=None, usecols=[4,5], names=['Old Star Sign', 'DateRange'])]).dropna()
old_star['Begin Date'] = old_star['DateRange'].apply(lambda x: pd.to_datetime('2020/'+re.search('^(\d+/\d+)', x).group(1),format='%Y/%m/%d').date())
old_star['End Date'] = old_star['DateRange'].apply(lambda x: pd.to_datetime('2020/'+re.search('(\d+/\d+)$', x).group(1),format='%Y/%m/%d').date())
old_star['End Date'] = old_star.apply(lambda x: x['End Date'].replace(year=2021) if x['End Date']<x['Begin Date'] else x['End Date'], axis=1)

new_star= pd.read_csv(r"F:\Data\New Star Signs.csv", header=None, names=['SignStr'])
new_star['New Star Sign'] = new_star['SignStr'].apply(lambda x: re.search('^(\w+)', x).group(1))
new_star['From Date'] = new_star['SignStr'].apply(lambda x: pd.to_datetime('2020'+re.findall('(\w+)\s\d+', x)[0][0:3]+re.findall('\w+\s(\d+)', x)[0],format='%Y%b%d').date())
new_star['To Date'] = new_star['SignStr'].apply(lambda x: pd.to_datetime('2020'+re.findall('(\w+)\s\d+', x)[1][0:3]+re.findall('\w+\s(\d+)', x)[1],format='%Y%b%d').date())
new_star['Date Range'] = new_star['SignStr'].apply(lambda x: re.findall('\w+\s(\d+)', x)[0]+' '+re.findall('(\w+)\s\d+', x)[0][0:3]+' - '+
                                                               re.findall('\w+\s(\d+)', x)[1]+' '+re.findall('(\w+)\s\d+', x)[1][0:3])
new_star['To Date'] = new_star.apply(lambda x: x['To Date'].replace(year=2021) if x['To Date']<x['From Date'] else x['To Date'], axis=1)

all_date = pd.read_csv(r"F:\Data\Scaffold.csv", parse_dates=['Date'], date_parser=lambda x: datetime.strptime(x, '%d/%m/%Y'))
all_date['Date']=all_date['Date'].dt.date
all_date['Birthday']=all_date['Date'].apply(lambda x: x.strftime('%b %d'))

all_date['dummy'] = 1
old_star['dummy'] = 1
new_star['dummy'] = 1 

temp = pd.merge(all_date, old_star, on='dummy')
olddate = temp[(temp['Date']>=temp['Begin Date']) & (temp['Date']<=temp['End Date'] )].copy()
temp = pd.merge(all_date, new_star, on='dummy')
newdate = temp[(temp['Date']>=temp['From Date']) & (temp['Date']<=temp['To Date'] )].copy()

final = pd.merge(olddate, newdate, on='Birthday')[['Birthday', 'Old Star Sign', 'New Star Sign', 'Date Range']].copy()
final['The Same'] = final.apply(lambda x: int(x['Old Star Sign']==x['New Star Sign']), axis=1)  
final['The Same Cases'] = final['The Same'].groupby(final['Birthday']).transform('max')
final = final[final['The Same Cases']==0][['Birthday', 'Old Star Sign', 'New Star Sign', 'Date Range']].copy()
