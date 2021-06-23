import pandas as pd

xlsx = pd.ExcelFile("F:/Data/NPS Input.xlsx")

temp = []
for sheet in xlsx.sheet_names:
    df = pd.read_excel(xlsx,sheet)
    temp.append(df)
like = pd.concat(temp)   
like.columns = ['Airline', 'CustomerID', 'like']
like['RespCount'] = like['CustomerID'].groupby(like['Airline']).transform('count')
like = like[like['RespCount']>=50].copy()

like['Class'] = like['like'].apply(lambda x: 'Detractors' if x<=6 else 'Passive' if x<=8 else 'Promoters') 

final = like.pivot_table(index='Airline', columns='Class', values='CustomerID', aggfunc='count').reset_index()
final['Promoters%'] = final.apply(lambda x: int(x['Promoters']/(x['Promoters']+x['Passive']+x['Detractors'])*100), axis=1)
final['Detractors%'] = final.apply(lambda x: int(x['Detractors']/(x['Promoters']+x['Passive']+x['Detractors'])*100), axis=1)
final['NPS'] = final['Promoters%'] - final['Detractors%']
final['Z-Score'] = round((final['NPS']-final['NPS'].mean())/final['NPS'].std(),2)
final = final[final['Airline']=='Prep Air'][['Airline', 'NPS', 'Z-Score']].copy()
