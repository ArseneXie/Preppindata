import pandas as pd

xlsx = pd.ExcelFile(r"C:\Data\PreppinData\Trilogies Input.xlsx")

top30 = pd.read_excel(xlsx,'Top 30 Trilogies')
top30['Trilogy'] = top30['Trilogy'].str.replace('\s+trilogy$','', regex=True)

films = pd.read_excel(xlsx,'Films')
temp = films['Number in Series'].str.split('/', n = 1, expand = True) 
films['Film Order'] = temp[0].astype('int64') 
films['Total Films in Series'] = temp[1].astype('int64') 
films['Trilogy Average'] = films['Rating'].groupby(films['Trilogy Grouping']).transform('mean')
films['Trilogy Highest'] = films['Rating'].groupby(films['Trilogy Grouping']).transform('max')
sort_cols = ['Trilogy Average', 'Trilogy Highest']
films['Trilogy Ranking'] = films.sort_values(sort_cols, ascending=False).groupby(sort_cols, sort=False).ngroup() + 1

final = pd.merge(films, top30, on='Trilogy Ranking').sort_values('Trilogy Ranking')
final['Trilogy Average'] = round(final['Trilogy Average'],1)
final = final[['Trilogy Ranking','Trilogy','Trilogy Average','Film Order','Title','Rating','Total Films in Series']].copy()
