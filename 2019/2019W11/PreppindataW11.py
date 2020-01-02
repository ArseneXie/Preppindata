import pandas as pd
from datetime import datetime

jdata = pd.read_csv("E:\PD - JSON DATA Stock data.csv").dropna()
jdata['Row']=jdata.apply(lambda x: [x for x in x['JSON_Name'].split('.')][::-1][0],axis=1)
jdata['DataType']=jdata.apply(lambda x: [x for x in x['JSON_Name'].split('.')][::-1][1] ,axis=1)
jdata['Category']=jdata.apply(lambda x: [x for x in x['JSON_Name'].split('.')][3] ,axis=1)

final = jdata[jdata['Category'] != 'meta'][['Row','DataType','JSON_ValueString']].copy()
final = final.pivot_table(index = ['Row'],
                          columns='DataType',
                          values='JSON_ValueString',
                          aggfunc='max')
final.reset_index(inplace = True)
final['Date']=final.apply(lambda x: datetime.utcfromtimestamp(int(x['timestamp'])).strftime('%Y-%m-%d %H:%M:%S') ,axis=1)
final=final[['Date','volume','high','low','adjclose','close','open','Row']]
