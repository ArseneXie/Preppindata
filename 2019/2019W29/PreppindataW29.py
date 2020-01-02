import pandas as pd

customer = pd.read_excel(pd.ExcelFile(r"E:\PD - Week 29 Input.xlsx"),"Customers")
customer['Packages'] = customer['Packages'].apply(lambda x: f'{x} '.strip() )
freq = pd.read_excel(pd.ExcelFile(r"E:\PD - Week 29 Input.xlsx"),"Subscription Packages") 
pkgs = pd.read_excel(pd.ExcelFile(r"E:\PD - Week 29 Input.xlsx"),"Subscription Products").astype({"Subscription Package": str}) 

ann_freq = pd.Series([52,12,4,1], index=freq.index)
freq['Freq Annum'] = ann_freq
freq.drop('Frequency', axis=1, inplace=True)
freq.rename(columns={'Subscription Package': 'Frequency'}, inplace=True)

subs = pd.concat([customer, 
                   pd.DataFrame([x for x in customer['Packages'].str.split('|').values.tolist()])], axis=1, sort=False)
subs = subs.melt(id_vars=[c for c in customer.columns], 
                 value_name='Subscription Package', var_name='To_drop').drop(['To_drop','Packages'], axis=1)
subs = subs.dropna(subset=['Subscription Package'])

subs = pd.merge(subs, freq, how='inner', on='Frequency')
subs = pd.merge(subs, pkgs, how='inner', on='Subscription Package')


wavg = subs[subs['Product'] != 'Mystery'].copy()
wavg_price = (wavg['Freq Annum']*wavg['Price']).sum() / wavg['Freq Annum'].sum()//1
subs.fillna(wavg_price,inplace=True)

final1=subs[['Subscription Package','Product','Price']].astype({'Price': int}).drop_duplicates()

subs['Subscription Cost(Annum)'] = subs['Freq Annum']*subs['Price']
final2=subs.groupby('Name',as_index=False).agg({'Subscription Cost(Annum)':'sum'})
