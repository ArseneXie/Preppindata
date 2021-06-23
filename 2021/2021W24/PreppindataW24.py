import pandas as pd
from datetime import timedelta

def timeoff(df, d):
    return len(df[(df['Start Date']<=d) & (d<=df['End Date'])])

df = pd.read_excel(pd.ExcelFile("F:/Data/Absenteeism Scaffold.xlsx"),'Reasons')
df['End Date'] = df.apply(lambda x: x['Start Date']+timedelta(days=x['Days Off']-1), axis=1)

final = pd.DataFrame(pd.date_range(start='2021/4/1', end='2021/5/31'), columns=['Date'])
final['Number of people off each day'] = final['Date'].apply(lambda x: timeoff(df,x))

ans1 = final[final['Number of people off each day']==max(final['Number of people off each day'])]['Date'].copy().iloc[0]
ans2 = len(final[final['Number of people off each day']==0])
