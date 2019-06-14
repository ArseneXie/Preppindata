import pandas as pd

xls = pd.ExcelFile(r"E:\anime.xlsx")

anime = pd.read_excel(xls,"anime") 
anime.drop(['episodes'],axis=1,inplace = True)
temp = anime[((anime['type'] == 'TV') | (anime['type'] == 'Movie')) & (anime['members'] >= 10000)].dropna().copy()
genre_split = pd.DataFrame([x for x in temp['genre'].str.split(',').values.tolist()])

final = pd.concat([temp[['name','genre','type','rating','members']].reset_index(drop=True), genre_split], axis=1, sort=False)
final.drop(['genre'],axis=1,inplace = True)
final = pd.melt(final, id_vars=['name','type','rating','members'], value_name='Genre')
final['Genre'] = final['Genre'].str.strip()
final.drop(['variable'],axis=1,inplace = True)
final=final.dropna()
final['Avg Rating'] = round((final.groupby(['Genre','type']))['rating'].transform('mean'),2)
final['Avg Viewers'] = round((final.groupby(['Genre','type']))['members'].transform('mean'))
final = final.groupby(['Genre','type']).apply(lambda t: t[t.rating==t.rating.max()])

final.drop(['members'],axis=1,inplace = True)
final.rename(columns={'type': 'Type', 'name': 'Prime Example', 'rating' : 'Max Rating'}, inplace=True)
final = final[['Genre','Type','Avg Rating','Max Rating','Avg Viewers','Prime Example']].reset_index(drop=True)
