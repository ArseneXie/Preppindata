import pandas as pd

travel = pd.read_csv(r'C:/Data/PreppinData/PD 2021 WK 1 to 4 ideas - Preferences of Travel.csv')
travel = travel.melt(id_vars='Student ID', value_name='Method of Travel', var_name='Weekday')

method_fix = {'Bicycle':'^B.*', 'Car':'^Ca.*', 'Helicopter':'^Hel.*', 'Scooter':'^Sco.*', 'Walk':'^W.*'}
travel['Method of Travel'] = travel['Method of Travel'].replace(list(method_fix.values()), list(method_fix.keys()), regex = True)

final = travel.groupby(['Weekday', 'Method of Travel'], as_index=False).agg({'Student ID':'count'})
final = final.rename(columns={'Student ID':'Number of Trips'})
final['Trips per Day'] = final['Number of Trips'].groupby(final['Weekday']).transform('sum')
final['% of trips per day'] = round(final['Number of Trips']/final['Trips per Day'], 2)

non_sustainable = ['Car', 'Van', 'Aeroplane', 'Helicopter']
final['Sustainable?'] = final['Method of Travel'].apply(lambda x: 'Non-Sustainable' if x in non_sustainable else 'Sustainable')
final = final.sort_values(['Weekday', 'Sustainable?'])
final = final[['Sustainable?', 'Method of Travel', 'Weekday', 'Number of Trips', 'Trips per Day', '% of trips per day']]
