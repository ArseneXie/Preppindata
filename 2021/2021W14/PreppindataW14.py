import pandas as pd
import re

xlsx = pd.ExcelFile("F:/Data/Week 14 - Input.xlsx")
out_file = "F:/Data/prepindata2021w14py.xlsx"

passenger = pd.read_excel(xlsx,sheet_name='Passenger List').rename(columns={'flight_number':'FlightNo.'})
passenger = passenger.drop([t for t in passenger.columns if re.match('^Unnamed',str(t))],axis=1)

seat = pd.read_excel(xlsx,sheet_name='SeatList')
seat = seat.melt(id_vars='Row', value_name='passenger_number', var_name='Seat')
seat['Seat Position'] = seat['Seat'].apply(lambda x: 'Window' if x in ('A','F') else 'Middle' if  x in ('B','E') else 'Aisle') 

flight = pd.read_excel(xlsx,sheet_name='FlightDetails')
flight.columns = ['infostr']
flight['FlightNo.'] = flight['infostr'].apply(lambda x: int(re.search('\[(\d+)',x).group(1)))
flight['Depart Hour'] = flight['infostr'].apply(lambda x: int(re.search('\|(\d+):',x).group(1)))
flight['Depart Time of Day'] = flight['Depart Hour'].apply(lambda x: 'Morning' if x<12 else 'Evening' if x>18 else 'Afternoon')

plane = pd.read_excel(xlsx,sheet_name='PlaneDetails')
plane['RowRule'] = plane['Business Class'].apply(lambda x: int(re.search('(\d+)$',x).group(1)))

df = pd.merge(passenger, seat, on='passenger_number')
df = pd.merge(df, flight[['FlightNo.', 'Depart Time of Day']], on='FlightNo.')
df = pd.merge(df, plane[['FlightNo.', 'RowRule']], on='FlightNo.')
df['Business Class'] = df.apply(lambda x: 'Economy' if x['Row']>x['RowRule'] else 'Business Class', axis=1) 
df['Purchase Amount'] = df.apply(lambda x: x['purchase_amount'] if x['Business Class']=='Economy' else 0, axis=1) 

finA = df.groupby('Depart Time of Day', as_index=False).agg({'Purchase Amount':'sum', 'FlightNo.':'nunique'})
finA['Avg per Flight'] = finA['Purchase Amount']/finA['FlightNo.']  
finA['Rank'] =  finA['Avg per Flight'].rank(ascending=False).astype(int)
finA = finA[['Rank', 'Depart Time of Day', 'Avg per Flight']].sort_values('Rank')

finB = df.groupby('Seat Position', as_index=False).agg({'Purchase Amount':'sum'})
finB['Rank'] =  finB['Purchase Amount'].rank(ascending=False).astype(int)
finB = finB[['Rank', 'Seat Position', 'Purchase Amount']].sort_values('Rank')

finC = df.groupby('Business Class', as_index=False).agg({'purchase_amount':'sum'}).rename(columns={'purchase_amount':'Purchase Amount'})
finC['Rank'] =  finC['Purchase Amount'].rank(ascending=False).astype(int)
finC = finC[['Rank', 'Business Class', 'Purchase Amount']].sort_values('Rank')

with pd.ExcelWriter(out_file) as writer:  
    finA.to_excel(writer, sheet_name='Time of day', index=False)  
    finB.to_excel(writer, sheet_name='Seat position', index=False)  
    finC.to_excel(writer, sheet_name='Business or Economy', index=False)  
