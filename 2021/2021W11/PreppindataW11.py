import pandas as pd

xlsx = pd.ExcelFile("F:/Data/Cocktails Dataset.xlsx")

cocktail = pd.read_excel(xlsx,sheet_name='Cocktails').rename(columns={'Price (£)':'Price'})
cocktail = pd.concat([cocktail.drop('Recipe (ml)', axis=1), 
                      pd.DataFrame([map(str.strip, x) \
                                    for x in cocktail['Recipe (ml)'].str.split(';').values.tolist()])],
                     axis=1, sort=False)
cocktail = cocktail.melt(id_vars=['Cocktail', 'Price'], value_name='Recipe', var_name='ToDrop')\
    .drop('ToDrop', axis=1).dropna().reset_index(drop=True)
cocktail['Ingredient'] = cocktail['Recipe'].str.extract('([\w\s]+)')   
cocktail['Measurement'] = cocktail['Recipe'].str.extract('(\d+)').astype(int)
    
curr_rate =  pd.read_excel(xlsx,sheet_name='Conversion Rates').set_index('Currency').T.to_dict('records')[0]
sourcing = pd.read_excel(xlsx,sheet_name='Sourcing')
sourcing['Unit Price'] = sourcing.apply(lambda x: x['Price']/curr_rate.get(x['Currency'])/x['ml per Bottle'], axis=1)

final = pd.merge(cocktail, sourcing[['Ingredient', 'Unit Price']], on='Ingredient')
final['Cost'] = final['Unit Price']*final['Measurement']
final = final.groupby(['Cocktail', 'Price'], as_index=False).agg({'Cost':'sum'})
final['Cost'] = round(final['Cost'], 2)
final['Margin'] = final['Price'] - final['Cost'] 
