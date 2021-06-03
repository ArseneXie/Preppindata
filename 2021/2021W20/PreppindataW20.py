import pandas as pd
from datetime import datetime as dt

out_file = "F:/Data/prepindata2021w20py.xlsx"

complaints = pd.read_csv("F:/Data/Prep Air Complaints - Complaints per Day.csv",
                         parse_dates=['Date'], date_parser=lambda x: dt.strptime(x, '%d/%m/%Y'))
complaints['Date'] = complaints['Date'].dt.date
complaints['Mean'] = complaints['Complaints'].groupby([complaints['Week']]).transform('mean')
complaints['Standard Deviation'] = complaints['Complaints'].groupby([complaints['Week']]).transform('std')

with pd.ExcelWriter(out_file) as writer:  
    for i in range(3):
        df = complaints.copy()
        df['Lower Control Limit'] = df['Mean'] - df['Standard Deviation']*(i+1)
        df['Upper Control Limit'] = df['Mean'] + df['Standard Deviation']*(i+1)
        df['Variation'] = df['Upper Control Limit'] - df['Lower Control Limit']
        df['Outlier'] = df.apply(lambda x: 'Inside' if x['Upper Control Limit']>=x['Complaints']>=x['Lower Control Limit'] else 'Outside', axis=1)
        df = df[df['Outlier']=='Outside']
        df.to_excel(writer, sheet_name=f'{i+1}SD', index=False)  
