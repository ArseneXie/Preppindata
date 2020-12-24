import pandas as pd
import re

xlsx = pd.ExcelFile("F:/Data/NBA Travel Distances.xlsx")

distance = pd.read_excel(xlsx,'Travel Distances')
distance = distance.rename(columns = {distance.columns[0]:'From City'})
distance = distance.melt(id_vars='From City', var_name='To City', value_name='Travel Time')
distance = distance[distance['Travel Time'] != 0].copy()
distance['Travel Time in Mins'] = distance['Travel Time'].apply(lambda x: 60*(int(re.search('(\d+)(?=h)',x).group(1)) if re.search('(\d+)(?=h)',x) else 0)+ 
                                                          (int(re.search('(\d+)(?=m)',x).group(1)) if re.search('(\d+)(?=m)',x) else 0))

league = pd.read_excel(xlsx,'League Structure')
league['City'] = league['Team'].apply(lambda x: re.search('(.*)(?=\s\w+$)',x.strip()).group(1))

final = pd.merge(league, distance, left_on='City', right_on='From City').rename(columns={c:'Home '+c for c in ['Team','Conference','Division','City']})
final = pd.merge(league[['City','Conference']], final, left_on='City', right_on='To City')
final['Travel Mins'] = final.apply(lambda x: x['Travel Time in Mins'] * (1.5 if x['Conference']==x['Home Conference'] else 1), axis=1)
final = final.groupby(['Home Team','Home Conference','Home Division'], as_index=False).agg({'Travel Mins':'sum'})
