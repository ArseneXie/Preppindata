import pandas as pd
import datetime

xlsx = pd.ExcelFile(r"C:\Data\PreppinData\2021W43 Input.xlsx")

unit_a = pd.read_excel(xlsx, 'Business Unit A ')
unit_a = unit_a.merge(pd.read_excel(xlsx, 'Risk Level'), left_on='Rating', right_on='Risk level')
unit_a['Date lodged'] = unit_a.apply(lambda x: f"{x['Date']}/{x['Month ']}/{x['Year']}", axis=1)
unit_a = unit_a[['Date lodged', 'Status', 'Risk rating']].rename(columns={'Risk rating':'Rating'})
unit_b = pd.read_excel(xlsx, 'Business Unit B ', skiprows=5)[['Date lodged', 'Status', 'Rating']]

rating = pd.concat([unit_a, unit_b]).rename(columns={'Status':'Status by Process'})
rating['Status by Lodged'] = rating['Date lodged'].apply(lambda x: 'Opening cases' 
                                                         if pd.to_datetime(x, format='%d/%m/%Y').date()<datetime.date(2021,10,1) else 'New cases')
rating = rating.melt(id_vars=['Rating','Date lodged'], value_name='Status', var_name='ToDrop').drop('ToDrop', axis=1)
rating = rating.pivot_table(index='Rating', columns='Status', values='Date lodged', aggfunc='count').reset_index().fillna(0)
rating = rating.rename(columns={'In Progress':'Continuing'})
rating = rating.melt(id_vars='Rating', value_name='Cases', var_name='Status').sort_values(['Rating','Status']) 
