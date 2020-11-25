import pandas as pd

xlsx = pd.ExcelFile("F:/Data/2020W47 Input.xlsx")

delays = pd.read_excel(xlsx,'Delays')
delays[['Airport','Type']] = delays[['Airport','Type']].ffill()
delays = delays.dropna().replace({'Airport':{'JKF':'JFK'}})
delays = delays.groupby(['Airport','Type'], as_index=False).agg({'RecordID':'count', 'Delay':'sum'})
delays = delays.rename(columns={'RecordID':'Delay flights'})

final = pd.merge(pd.read_excel(xlsx,'On Time'), delays, on=['Airport','Type'])
final['% Flights Delayed'] = round(final['Delay flights']/(final['Delay flights']+final['Number of flights '])*100,2)
final['Avg Delay (mins)'] = round(final['Delay']/(final['Delay flights']+final['Number of flights ']),2)
final = final[['Airport', 'Type', '% Flights Delayed', 'Avg Delay (mins)']]

#python rounding half to even.