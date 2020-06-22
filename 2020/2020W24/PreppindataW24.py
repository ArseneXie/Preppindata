import pandas as pd
import numpy as np
import re
import calendar
import datetime

mon_index = dict((v,k) for k,v in enumerate(calendar.month_abbr))

battle = pd.read_csv(r'F:/Data/Battles Input.csv',encoding='cp1252')
battle = pd.DataFrame([x for x in battle['DownloadData'].str.split('<br />').values.tolist()])
battle.columns = ['ToDrop', 'Battle', 'Date', 'War', 'Victors', 'Description', 'ToDrop2']
battle = battle.drop(['ToDrop','ToDrop2'],axis=1).replace(r'^\s*$', np.nan, regex=True).dropna()
battle['Battle'] = battle['Battle'].apply(lambda x: re.sub('<.*>','',x))
battle['Victors'] = battle['Victors'].apply(lambda x: re.sub('<.*>(Victors:\s)*','',x))
battle['Date'] = battle['Date'].apply(lambda x: re.sub('^(\d+)$', '1 Jan, \\1',
                                                        re.sub('^(\d+)\W+\d*\s*(\w+)\W*(\d+)','\\1 \\2, \\3', 
                                                               re.sub('^(\D+)\s(\d+)\D','\\2 \\1,',
                                                                      re.sub('\D+$','',x)))))
battle['Date'] = battle['Date'].apply(lambda x: datetime.date(int(re.search('(\d+)$',x).group(1)),
                                                              mon_index[re.search('\s(\w+)\W',x).group(1)[0:3]],
                                                              int(re.search('^(\d+)',x).group(1))))
