import pandas as pd

menu = pd.read_excel(pd.ExcelFile(r"E:\PD - Wk 26 Cocktails.xlsx"),"Sheet1") 
menu.columns = ['Cocktails','Ingredient','Cocktail Price']
final = pd.concat([menu, 
                   pd.DataFrame([map(str.strip, x) for x in menu['Ingredient'].str.split(',').values.tolist()])], axis=1, sort=False)
final = final.melt(id_vars=[c for c in menu.columns], value_name='Ingredient Split', var_name='Ingredient Position')
final = final.dropna(subset=['Ingredient Split'])
final.drop('Ingredient',axis=1,inplace=True)
final['Ingredient Position'] =  final['Ingredient Position']+1
final['Average Ingredient Price'] = final['Cocktail Price'].groupby(final['Ingredient Split']).transform('mean')
