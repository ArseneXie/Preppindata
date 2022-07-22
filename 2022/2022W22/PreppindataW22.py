import pandas as pd

xlsx = pd.ExcelFile(r"C:\Data\PreppinData\Critical_Role_Campaign_1_Datapack.xlsx")

eptime = pd.read_excel(xlsx, 'episode_details')[['Episode', 'runtime_in_secs']]
dialogue = pd.read_excel(xlsx, 'dialogue').merge(eptime, on='Episode') 


dialogue = dialogue[dialogue['Episode'].isin(['C1E001', 'C1E002'])]

dialogue = dialogue.sort_values(['Episode', 'time_in_secs'], ascending=True)


# test = dialogue.copy()
# dialogue = test.copy()

dialogue['next_time'] = dialogue['time_in_secs'].shift(-1)
dialogue['Duration'] = dialogue.apply(lambda x: (x['runtime_in_secs'] if pd.isna(x['next_time']) 
                                                 else x['next_time'])-x['time_in_secs'], axis=1) 
dialogue = dialogue.rename(columns={'time_in_secs':'start_time'})
dialogue = dialogue[dialogue['section']=='Gameplay'].reset_index(drop=True)
dialogue = pd.concat([dialogue.drop(['name', 'runtime_in_secs', 'next_time'], axis=1), 
                      pd.DataFrame([map(str.strip, x) for x in dialogue['name'].str.split(',').values.tolist()])],
    			  axis=1, sort=False)

dialogue.columns
# Preceding 3, self and following 3
final['Rolling Avg'] =  final.groupby('Destination')['Revenue'].transform(lambda x: x.rolling(7, 1).mean().shift(-3))
final['Rolling Total'] =  final.groupby('Destination')['Revenue'].transform(lambda x: x.rolling(7, 1).sum().shift(-3))
final['Rolling Avg2'] =  final.groupby('Destination')['Revenue'].transform(lambda x: x.shift(-3).rolling(7, 1).mean())
final['Rolling Total2'] =  final.groupby('Destination')['Revenue'].transform(lambda x: x.shift(-3).rolling(7, 1).sum())

final['Rolling Week Avg'] =  final.apply(lambda x: x['Rolling Avg2'] if pd.isna(x['Rolling Avg'])  else x['Rolling Avg'], axis=1)
final['Rolling Week Total'] =  final.apply(lambda x: x['Rolling Total2'] if pd.isna(x['Rolling Total'])  else x['Rolling Total'], axis=1)


orders = pd.read_excel(xlsx, 'Orders')
ord_cols = orders.columns
guest = [g for g in ord_cols if g[0:7]!='Unnamed']
select = {i:j for i,j in zip(ord_cols[:-1], ord_cols[1:]) if i[0:7]!='Unnamed'}

orders['Course'] = orders['Carl'].apply(lambda x: x if x in ['Starters', 'Mains', 'Dessert'] else None).ffill() 

for g in guest:
    orders[g] = orders.apply(lambda x: x[g] if pd.notna(x[select[g]]) else None, axis=1)

final = orders[['Course']+guest].melt(id_vars='Course', value_name='Dish', var_name='Guest').dropna()
final = final.merge(pd.read_excel(xlsx, 'Lookup Table'), on = 'Dish')[['Course', 'Guest', 'Recipe ID', 'Dish']]
final = final.sort_values(['Guest', 'Course'], ascending=[True, False])
