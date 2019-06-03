import pandas as pd
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import numpy as np

xls = pd.ExcelFile("E:\PD - Week 10 - Email Subscriptions.xlsx")
sign_up = pd.read_excel(xls,"Mailing List 2018") 
life_val = pd.read_excel(xls,"Customer Lifetime Value") 
unsub = pd.read_excel(xls,"Unsubscribe list") 
sign_up.rename(columns = {"Liquid": "Interested in Liquid Soap", 
                                  "Bar":"Interested In Soap Bars",}, inplace=True)
unsub["Unsubscribe date"] = unsub.apply(lambda x: pd.to_datetime(x["Date"], format='%d.%m.%Y'),axis=1)
unsub["possible key"] = unsub.apply(lambda x: x["first_name"][0:1].lower()+re.sub('[^a-z]','',x["last_name"].lower()),axis=1)

signup_val = sign_up.merge(life_val, on="email", how='inner')
signup_val['fuzzy'] = signup_val.apply(lambda x: process.extractOne(re.search('^[a-z]+(?=.*@)',x['email']).group(0), \
    unsub['possible key'],scorer=fuzz.ratio, score_cutoff = 85), axis=1)
signup_val['possible key'] = signup_val.apply(lambda x: x['fuzzy'][0] if x['fuzzy'] is not None else None, axis=1)

sub_wi_unsub = signup_val.merge(unsub, on="possible key", how='inner')
sub_wi_unsub.drop(['fuzzy','possible key','first_name','last_name','Date'],axis=1,inplace = True)
sub_wi_unsub['Status'] = sub_wi_unsub.apply(lambda x: 'Unsubscribed' if x['Unsubscribe date']>x['Sign-up Date'] else 'Resubscribed',axis=1)

sub_wo_unsub = signup_val[signup_val['possible key'].isnull()].copy()
sub_wo_unsub.drop(['fuzzy','possible key'],axis=1,inplace = True)
sub_wo_unsub['Status'] = 'Subscribed'
sub_wo_unsub['Unsubscribe date'] = None

finalA = pd.concat([sub_wi_unsub[sub_wi_unsub['Status']=='Resubscribed'],sub_wo_unsub],sort=False,ignore_index=True)

def get_group(mons):
    if mons >= 0 and mons <=3:        return '0-3'
    elif mons > 3 and mons <=6:       return '3-6'
    elif mons > 6 and mons <=12:      return '6-12'
    elif mons > 12 and mons <=24:     return '12-24'
    elif mons > 24:       return '24+'
    else:        return np.NaN
    
finalB = pd.concat([sub_wi_unsub,sub_wo_unsub],sort=False, ignore_index=True)
finalB['Unsubscribe date'] = pd.to_datetime(finalB['Unsubscribe date'])
finalB['Sign-up Date'] = pd.to_datetime(finalB['Sign-up Date'])
finalB['months'] = finalB.apply(lambda x: (x['Unsubscribe date']-x['Sign-up Date'])/np.timedelta64(1,'M'), axis=1)
finalB['months before unsubscribe'] =  finalB.apply(lambda x: get_group(x['months']), axis=1)
aggr = {     'email':'count',    'Liquid Sales to Date':'sum',    'Bar Sales to Date':'sum'}
finalB = finalB.astype(str).groupby(['months before unsubscribe','Status','Interested in Liquid Soap','Interested In Soap Bars'] \
                      , as_index=False).agg(aggr)



