import pandas as pd
import numpy as np

sales = pd.read_csv("F:\\Data\\PD 2021 Wk 32 Input - Data.csv",
                    parse_dates=['Date','Date of Flight'], 
                    date_parser=lambda x: pd.to_datetime(x, format='%d/%m/%Y'))

sales['Flight'] = sales['Departure'] + ' to ' + sales['Destination'] 
sales['Days'] = (sales['Date of Flight'] - sales['Date']).dt.days
sales['Days Category'] = sales['Days'].apply(lambda x: '7 days of more until the flight' if x>=7 else 'less than 7 days until the flight')
sales = sales[['Flight', 'Class', 'Ticket Sales', 'Days Category']].copy()

final = np.round(sales.pivot_table(index=['Flight', 'Class'], columns='Days Category',
                                   values='Ticket Sales',
                                   aggfunc={'Ticket Sales':[('Sales', np.sum), ('Avg. daily sales', np.mean)]})).reset_index()
final.columns = [(c[0]+' '+c[1]).strip() for c in final.columns]
final = final[['Flight','Class',
               'Avg. daily sales 7 days of more until the flight',
               'Avg. daily sales less than 7 days until the flight',
               'Sales less than 7 days until the flight',
               'Sales 7 days of more until the flight']]
