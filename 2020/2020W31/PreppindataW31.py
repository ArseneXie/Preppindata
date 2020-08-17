import pandas as pd
import re

xlsx = pd.ExcelFile("F:/Data/Medals PD WOW.xlsx")
medal = pd.read_excel(xlsx,'Medallists')   
code_map = {cl[0]:cl[1] for cl in pd.read_excel(xlsx,'Country Codes').to_dict('split')['data']}
country_map = {cl[1]:cl[0] for cl in pd.read_excel(xlsx,'Country Codes').to_dict('split')['data']}

medal['Code'] = medal.apply(lambda x: code_map.get(x['Country'],x['Country Code']), axis=1)
medal['Country'] = medal.apply(lambda x: country_map.get(x['Code'],x['Country']) if pd.isna(x['Country']) else x['Country'], axis=1)
medal = medal.dropna(subset=['Country','Code']).drop('Country Code', axis=1)
medal['Event'] = medal['Event'].apply(lambda x: re.sub('(?<!kilo)(metre(s*))','m',x))
medal['Event'] = medal['Event'].apply(lambda x: re.sub('(kilometre(s*))','km',x))
medal['Sport'] = medal['Sport'].apply(lambda x: re.sub('^Canoe.*','Canoeing',x))
medal['Sport'] = medal['Sport'].apply(lambda x: re.sub('^Swimming$','Aquatics',x))  
medal['Discipline'] = medal['Discipline'] .apply(lambda x: re.sub('Beach volley.*','Beach Volleyball',x))
medal['Discipline'] = medal['Discipline'] .apply(lambda x: re.sub('Wrestling.*','Wrestling',x))
medal['Discipline'] = medal['Discipline'] .apply(lambda x: re.sub('Rhythmic.*','Rhythmic',x))
medal['Discipline'] = medal['Discipline'] .apply(lambda x: re.sub('Artistic.*','Artistic',x))
medal['Discipline'] = medal['Discipline'] .apply(lambda x: re.sub('Mountain (B|b)ik.*','Mountain Bike',x))
medal['Discipline'] = medal['Discipline'] .apply(lambda x: re.sub('Modern (P|p)en.*','Modern Pentath.',x))
medal['Discipline'] = medal['Discipline'] .apply(lambda x: re.sub('(.*) cycling','Cycling \\1',x))

finalA = medal[['Country', 'Code', 'Sport', 'Medal', 'Event', 'Athlete', 'Year', 'Event_Gender', 'Discipline']].copy()

finalB = medal.pivot_table(index = ['Country','Year'],
                           columns= 'Medal',
                           values= 'Athlete',
                           aggfunc={'Athlete':'count'}).reset_index()
finalB = finalB[['Country', 'Year', 'Gold', 'Silver', 'Bronze']]

finalC = pd.read_excel(xlsx,'Hosts').astype({'Start Date': str, 'End Date': str})  
finalC['Start Date'] =  finalC['Start Date'].apply(lambda x: pd.to_datetime(x))
finalC['Start Date'] =  finalC['Start Date'].dt.date
finalC['End Date'] =  finalC['End Date'].apply(lambda x: pd.to_datetime(x))
finalC['End Date'] =  finalC['End Date'].dt.date
finalC['Year'] = finalC['Start Date'].apply(lambda x: x.year)
temp = finalC['Host'].str.split(',', n = 1, expand = True)
finalC['Host City'] = temp[0].str.strip()
finalC['Host Country'] = temp[1].str.strip()
finalC = finalC[['Year', 'Host Country', 'Host City', 'Start Date', 'End Date', 'Games', 'Nations', 'Sports', 'Events']].copy()
