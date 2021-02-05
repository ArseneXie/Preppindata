import pandas as pd

final = pd.read_csv(r'F:/Data/Joined Dataset.csv', parse_dates=['From Date'], date_parser=lambda x: pd.to_datetime(x, format='%d/%m/%Y'))
final['From Date'] = final['From Date'].dt.date
final = final.groupby(['Client ID']).apply(lambda x: x[x['From Date']==x['From Date'].max()]).reset_index(drop=True).copy()
