import pandas as pd

xlsx = pd.ExcelFile("F:/Data/Copy of Karaoke Dataset.xlsx")
kara = pd.read_excel(xlsx,sheet_name='Karaoke Choices')
customer = pd.read_excel(xlsx,sheet_name='Customers').astype({'Customer ID': str}) 

kara = kara.sort_values(by='Date').reset_index(drop=True)
kara['Seq'] = kara.index+1
kara['Time between Prev Songs'] = (kara['Date']-kara['Date'].shift(1)).astype('timedelta64[m]')
kara['Session #'] = kara.apply(lambda x: 1 if x['Seq']==1 or x['Time between Prev Songs']>=59 else 0, axis=1).cumsum()
kara['Song Order'] = kara['Seq'] - kara['Seq'].groupby(kara['Session #']).transform('min') + 1

entry_range = kara.groupby(['Session #'], as_index=False).agg({'Date':'min'})
entry_range['Date Early'] = entry_range['Date'].apply(lambda x: x+ pd.Timedelta(minutes=-10))
entry_range['dummy'] = 1
customer['dummy'] = 1
match = pd.merge(entry_range,customer,on='dummy')
match = match[(match['Entry Time']<=match['Date']) & (match['Entry Time']>=match['Date Early'])][['Session #','Customer ID']]

final = pd.merge(kara, match, how='left', on='Session #')
final = final[['Session #', 'Customer ID', 'Song Order', 'Date', 'Artist', 'Song']]
 