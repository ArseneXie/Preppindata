import pandas as pd
import re

final = pd.read_csv(r'C:/Data/PreppinData/PD 2023 Wk 1 Input.csv',
                    parse_dates=['Transaction Date'], date_parser=lambda x: pd.to_datetime(x, format='%d/%m/%Y %H:%M:%S'))

final['Bank'] = final['Transaction Code'].apply(lambda x: re.search('^([A-Z]+)',x).group(1))
final['Online or In-Person'] = final['Online or In-Person'].apply(lambda x: 'Online' if x==1 else 'In-Person')  
final['Transaction Date'] = final['Transaction Date'].dt.day_name()

output1 = final.groupby(['Bank'], as_index=False).agg({'Value':'sum'})
output2 = final.groupby(['Bank', 'Online or In-Person', 'Transaction Date'], as_index=False).agg({'Value':'sum'})
output3 = final.groupby(['Bank', 'Customer Code'], as_index=False).agg({'Value':'sum'})
