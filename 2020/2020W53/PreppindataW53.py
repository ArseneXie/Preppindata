import pandas as pd
import re
from math import sqrt

polygon_points = {'Round 1':[(1,0),(0,0),(0,1),(1,1)], 'Round 2':[(1,-1),(0,-1),(0,0),(1,0)],
                  'Round 3':[(0,-1),(-1,-1),(-1,0),(0,0)], 'Round 4':[(0,0),(-1,0),(-1,1),(0,1)]}

winner = pd.read_excel(pd.ExcelFile("F:/Data/USOpenWinners.xlsx"),sheet_name=0).drop('pos', axis=1)
winner.columns = [c.title() for c in winner.columns]
winner['Round Par'] = winner.apply(lambda x: round((x['Total']-(0 if x['To Par']=='E' else x['To Par']))/4), axis=1)
winner = winner.melt(id_vars=[c for c in winner.columns if not re.match('^(Round\s\d)$',c)], var_name='Round Num', value_name='Round Score').drop('To Par', axis=1)
winner['Round to Par'] = winner['Round Score'] - winner['Round Par'] 
for i in range(4):
    winner[f'Point{i+1}'] = winner['Round Num'].apply(lambda x: polygon_points[x][i])
winner = winner.melt(id_vars=[c for c in winner.columns if not re.match('^(Point\d)$',c)], var_name='Point', value_name='Coordinate')
winner['X Coordinate Polygon'] = winner.apply(lambda x: sqrt(x['Round Score'])*x['Coordinate'][0], axis=1)
winner['Y Coordinate Polygon'] = winner.apply(lambda x: sqrt(x['Round Score'])*x['Coordinate'][1], axis=1)
winner['Round Colors'] = winner['Round Num'].apply(lambda x: chr(64+int(re.search('(\d)$',x).group(1))))

location = pd.read_excel(pd.ExcelFile("F:/Data/Location Prize Money.xlsx"),sheet_name=0)[['Year', 'Country', 'Venue', 'Location']]

finalA = pd.merge(winner.drop('Coordinate', axis=1), location, on='Year')
finalA['Decade'] = finalA['Year'].apply(lambda x: x//10*10)
finalA['Row'] = finalA['Decade'].apply(lambda x: int((x - min(finalA['Decade']))/10+1))
finalA['Column'] = finalA['Year'] - finalA['Decade'] + 1 

finalB = finalA.groupby('Decade',as_index=False).agg({'Round Score':[('Min Round Score', 'min'), ('Max Round Score', 'max')],
                                                      'Total':[('Min Total Score', 'min'), ('Max Total Score', 'max')]})
finalB.columns = [col[1] if col[1] else col[0] for col in finalB.columns.values]
