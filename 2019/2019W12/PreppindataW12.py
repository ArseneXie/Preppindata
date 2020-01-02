import pandas as pd
from datetime import timedelta

xls = pd.ExcelFile("E:\PD12 - System errors.xlsx")

autolog = pd.read_excel(xls,"Automatic Error log") 
manlog = pd.read_excel(xls,"Manual capture error list") 

for k in ['Start','End']:
    manlog[k+'DateTime'] = manlog.apply(lambda x: pd.to_datetime(x[k+' Date'].strftime('%Y-%m-%d')+' '+ x[k+' Time'].strftime('%H:%M:%S')),axis=1)
    autolog[k+'DateTime'] = autolog.apply(lambda x: x[k+' Date / Time']+timedelta(hours=0.5)*(1 if k=='End' else -1),axis=1)
    manlog.drop([k+' Date',k+' Time'],axis=1,inplace = True)

df_dup = pd.merge(manlog, autolog, on='System',suffixes=('_man', '_auto'))
df_dup = df_dup.query('StartDateTime_auto <= StartDateTime_man and EndDateTime_auto >= EndDateTime_man') 

final = pd.merge(autolog, df_dup, how='left', on=['System','Start Date / Time','End Date / Time'])
final = final[['System','Error','Start Date / Time','End Date / Time','StartDateTime_man','EndDateTime_man']].copy()

final = pd.merge(final,manlog, how='outer', left_on=['System','StartDateTime_man','EndDateTime_man'], \
                 right_on=['System','StartDateTime','EndDateTime'] ,suffixes=('_a', '_m'), indicator='Check')

for k in ['Start','End']:
    final[k+' Date / Time'] = final.apply(lambda x: x[k+'DateTime'] if pd.isnull(x[k+' Date / Time']) else x[k+' Date / Time'],axis=1)
    final.drop([k+'DateTime',k+'DateTime_man'],axis=1,inplace = True)
final['Error'] = final.apply(lambda x: x['Error_m'] if pd.isnull(x['Error_a']) else x['Error_a'],axis=1)
final['Error source'] = final.apply(lambda x: 'Manual capture error list' if x['Check']=='right_only' else 'Automatic Error log',axis=1)
final['Downtime in Hours'] = final.apply(lambda x: (x['End Date / Time']-x['Start Date / Time'])/timedelta(minutes=60),axis=1)    
final['Total Downtime in Hours'] = final['Downtime in Hours'].groupby(final['System']).transform('sum')
final['% of system downtime'] = final['Downtime in Hours']/final['Total Downtime in Hours']  
final.drop(['Error_m','Error_a','Check'],axis=1,inplace = True)
