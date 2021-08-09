import pandas as pd
import re

xlsx = pd.ExcelFile("F:/Data/Olympic Events.xlsx")
sport_pt = {'Artistic Gymnastics':'^Artistic Gymnastic.*', 'Baseball/Softball':'^(Baseball|Softball).*', 'Beach Volleyball':'^Beach Volley.*',
            'Boxing':'^Boxing.*', 'Rugby':'^Rugby.*', 'Skateboarding':'^Skateboarding.*', 'Wrestling':'^Wrestling.*'}
events = pd.read_excel(xlsx,'Olympics Events')
events['Date'] = events['Date'].apply(lambda x: re.sub('(\d+).+_(\w+)_(\d+)','\\1 \\2 \\3',x)) 
events['UK Date Time'] = events.apply(lambda x: x['Date']+' '+('0:00' if x['Time']=='xx' else x['Time']), axis=1)
events['Date'] = events['Date'].apply(lambda x: pd.to_datetime(x, format='%d %B %Y').date())
events['UK Date Time'] = events['UK Date Time'].apply(lambda x: pd.to_datetime(x, format='%d %B %Y %H:%M'))
for correct, pattern in sport_pt.items():
    events['Sport'] = events['Sport'].str.title().replace(to_replace = pattern, value = correct, regex = True)

events = pd.concat([events[['Date', 'UK Date Time', 'Sport', 'Venue']], 
                   pd.DataFrame([map(str.strip, x) \
                                 for x in events['Events'].str.split(',').values.tolist()])],
                  axis=1, sort=False)
events = events.melt(id_vars=[c for c in events.columns if not re.match('^\d', str(c))],
                          value_name='Event', var_name='ToDrop')\
                              .drop('ToDrop', axis=1).dropna(subset=['Event']).reset_index(drop=True)
events['Medal Ceremony?'] = events['Event'].apply(lambda x: bool(re.search('Victory Ceremony', x)) or bool(re.search('Gold Medal', x)))  
events['Venue'] =  events['Venue'].str.title()                            

venues = pd.read_excel(xlsx,'Venues')[['Venue', 'Location']].drop_duplicates()
temp = venues['Location'].str.split(',', n = 1, expand = True) 
venues['Latitude'] = temp[0].astype('float') 
venues['Longitude'] = temp[1].astype('float') 
venues = venues.drop('Location', axis=1)
venues['Venue'] =  venues['Venue'].str.title()   

final = pd.merge(events, venues, on='Venue')
final = final[['UK Date Time', 'Date', 'Sport', 'Event', 'Medal Ceremony?', 'Venue', 'Latitude', 'Longitude']]
