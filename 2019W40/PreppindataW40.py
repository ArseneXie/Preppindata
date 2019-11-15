import pandas as pd
import numpy as np
import re

food_rate = [None, 'Horrendous','Just about edible but I was hungry','Some good, some not so good','Yum!','Give the team a Michelin star!!']
xls = pd.ExcelFile("E:/Sudzilla Conference feedback (Responses).xlsx")
resp = pd.read_excel(xls,xls.sheet_names[0])

nps = pd.DataFrame([{'Promoter':len(resp[resp['On a scale of 0-10, how would you rate Sudzilla?']>=9]),
                     'Detractor':len(resp[resp['On a scale of 0-10, how would you rate Sudzilla?']<=6]),
                     'Total Respondents':len(resp)}])
nps['NPS Score'] = round((nps['Promoter']-nps['Detractor'])/nps['Total Respondents']*100,1)

resp['food1'] = resp['How would you rate the food at Sudzilla (breakfast)?'].apply(lambda x:food_rate.index(x) if not pd.isnull(x) else x)
resp['food2'] = resp['How would you rate the food at Sudzilla (lunch)?'].apply(lambda x:food_rate.index(x) if not pd.isnull(x) else x)
resp['food3'] = resp['How would you rate the food at Sudzilla (dinner)?'].apply(lambda x:food_rate.index(x) if not pd.isnull(x) else x)
resp['Food Rating Score'] = resp.apply(lambda x:np.nanmean([x['food1'],x['food2'],x['food3']]),axis=1)
resp['Keynote Rating Score'] = resp.apply(lambda x:np.nanmean([x['On a scale of 0-10, how would you rate the opening keynote?'],
                                                              x['On a scale of 0-10, how would you rate the closing keynote?']]),axis=1)
detail = resp[['Timestamp', 
             'On a scale of 0-10, how would you rate Sudzilla?',
             '...why?',
             'Which three words would you use describe to Sudzilla? (separate with a comma)',
             'What was your favourite giveaway at Sudzilla?',
             "What was your favourite 'Soap Box' (breakout / customer speaker) session?",
             'Food Rating Score', 
             'Keynote Rating Score']].copy()
detail = pd.concat([detail, 
                    pd.DataFrame([map(str.strip, x) \
                                 for x in detail['Which three words would you use describe to Sudzilla? (separate with a comma)'].str.split(',').values.tolist()])],
 axis=1, sort=False)
detail = detail.melt(id_vars=[c for c in detail.columns if not re.match('^\d', str(c))],
                          value_name='Which three words', var_name='ToDrop')\
                              .drop('ToDrop', axis=1).dropna(subset=['Which three words']).reset_index(drop=True)
detail['Which three words would you use describe to Sudzilla? (separate with a comma)'] = detail['Which three words'].apply(lambda x: re.sub('\W+$','',x))
detail.drop('Which three words', axis=1, inplace=True)
