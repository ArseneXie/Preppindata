import pandas as pd

xlsx = pd.ExcelFile(r"C:\Data\PreppinData\Menu Input.xlsx")

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
