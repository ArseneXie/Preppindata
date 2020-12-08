import pandas as pd
import re

xlsx = pd.ExcelFile("F:/Data/2020W48 Input.xlsx")

stand = pd.read_excel(xlsx,'Stands')
stand = pd.concat([stand, 
                   pd.DataFrame([map(str.strip, x) \
                                 for x in stand['Accessed by Gates'].str.split(',').values.tolist()])],
                  axis=1, sort=False)
stand = stand.melt(id_vars=[c for c in stand.columns if not re.match('^\d', str(c))], value_name='Gate', var_name='To_drop').dropna()
stand['OneGate'] = stand['Accessed by Gates'].apply(lambda x: 'N' if re.search('(,)',x) else 'Y')
stand = pd.merge(stand.drop(['Accessed by Gates','To_drop'], axis=1), pd.read_excel(xlsx,'Remote Stands Accesibility'), on='Gate')
stand['Stand'] = stand['Stand'].apply(lambda x: int(re.search('(\d+)$',x).group(1)))
stand['Gate'] = stand['Gate'].apply(lambda x: int(re.search('(\d+)$',x).group(1)))
flight = pd.merge(stand, pd.read_excel(xlsx,'Stand Allocations 01.02.2020 AM', dtype={'Time':str}), on='Stand')
flight['Date Begin'] = flight['Time'].apply(lambda x: pd.to_datetime('01.02.2020.'+x, format='%d.%m.%Y.%H%M'))
flight['Date End'] = flight['Date Begin'].apply(lambda x: x+pd.Timedelta(minutes=45))
flight['Time factor'] = flight.apply(lambda x: x['Time to Reach Remote Stands'] * (-1 if x['Requires Bus?']=='Y' else 1), axis=1)
flight = flight.sort_values(['OneGate', 'Requires Bus?','Time factor','Flight'], ascending=[False, False, False, True])

gateall = pd.read_excel(xlsx,'Gate Availability')
gateall['Flight'],gateall['Stand'],gateall['Requires Bus?'],gateall['Time to Reach Stand'] = [None,None,None,None]
allocated = []
for _, row in flight.iterrows():
    if row['Flight'] in allocated:
        continue
    available = gateall[(gateall['Gate']==row['Gate']) & (gateall['Date']>=row['Date Begin']) & (gateall['Date']<row['Date End']) & pd.isnull(gateall['Flight'])]
    if len(available)==3:
        allocated.append(row['Flight'])
        gateall.loc[available.index,['Flight','Stand','Requires Bus?','Time to Reach Stand']] = \
            [row['Flight'],row['Stand'],row['Requires Bus?'],0 if row['Requires Bus?']=='N' else row['Time to Reach Remote Stands']]
    else:    
        continue

final = gateall[['Gate', 'Stand', 'Date', 'Flight', 'Requires Bus?', 'Time to Reach Stand']].copy()
