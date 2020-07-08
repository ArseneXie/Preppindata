import pandas as pd

xlsx = pd.ExcelFile("F:/Data/Input.xlsx")

ppr = pd.read_excel(xlsx,'Preppers')   
loc = pd.read_excel(xlsx,'Location')
info = pd.read_excel(xlsx,'Information',skiprows=1).dropna(subset=['Rating'])

rel_val = {'Rarely Breaks':1, 'Inconsistent':2, 'Fairly Inconsistent':3, 'Fairly Consistent':4, 'Very Consistent':5}

loc['Site'] = loc['Site'].apply(lambda x: x.split('-')[0].strip())
loc['Dummy'] = 0
ppr['Dummy'] = 0

final = ppr.merge(loc, on='Dummy')
final['Check'] = final.apply(lambda x: len(set(map(str.strip,x['Season'].split(','))) & set(map(str.strip,x['Surf Season'].split(',')))), axis=1)
final = final[final['Check'] > 0].drop(['Dummy','Season'],axis=1).copy()

final = final.merge(info, left_on='Site', right_on='Surf Site')
final['Check'] = final.apply(lambda x: len(set(map(str.strip,x['Board Type'].split(','))) & set(map(str.strip,x['Boards'].split(',')))) *
                             len(set(map(str.strip,x['Skill'].split(','))) & set(map(str.strip,x['Skill Level'].split(',')))) , axis=1)
final = final[final['Check'] > 0].drop(['Check','Skill','Board Type','Site'],axis=1).copy()

final['RatingRel'] = final.apply(lambda x: x['Rating'] + rel_val[x['Reliability']]/100, axis=1)
final = final.loc[final.groupby('Name')['RatingRel'].idxmax()][['Name', 'Surf Site', 'Swell Direction', 'Reliability', 'Wind Direction', 
                                                                'Type', 'Boards', 'Skill Level', 'Surf Season','Rating']].copy()
