import pandas as pd

xlsx = pd.ExcelFile(r"C:\Data\PreppinData\Carl's 2021 cycling.xlsx")
cycling = pd.read_excel(xlsx)
cycling['Measure'] = cycling['Measure'].apply(lambda x: 'Outdoors' if x=='km' else 'Turbo Trainer') 
cycling['Activity per day'] = cycling['Type'].groupby(cycling['Date']).transform('count')
cycling = cycling.pivot_table(index= ['Date', 'Activity per day'],
                              columns='Measure', values='Value', aggfunc=sum).reset_index()
cycling.index = pd.DatetimeIndex(cycling['Date'])
cycling = cycling.reindex(pd.date_range(cycling.index.min(), cycling.index.max())).rename_axis('FillDate').reset_index()
cycling['Date'] = cycling['FillDate'].dt.date 
cycling = cycling[['Date', 'Activity per day', 'Turbo Trainer', 'Outdoors']].fillna(0)
