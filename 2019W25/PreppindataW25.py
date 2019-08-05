import pandas as pd
import re

gigs = pd.read_excel(pd.ExcelFile(r"E:\Wow _ PD data set.xlsx"),"Gigs Data") 
gigs['Concert Date'] = gigs['Concert Date'].apply(lambda x: x.date())
gigs.drop(['ConcertID'],axis=1,inplace=True)
gigs_ci = gigs.apply(lambda x: x.astype(str).str.lower()).drop_duplicates()  #1545 rows --> 1141 rows
gigs = gigs.loc[gigs_ci.index]
gigs = gigs.reset_index(drop=True)
gigs['All Artists']=gigs.apply(lambda x: x['Concert'] if re.search('\/',str(x['Concert'])) else x['Artist'],axis=1) 

home =  pd.read_excel(pd.ExcelFile(r"E:\Wow _ PD data set.xlsx"),"Home Locations")
home.rename(columns={'Longitude':'Home Longitude', 'Latitude':'Home Latitude'}, inplace = True)

loc = pd.read_csv("E:\LongLats.csv")
temp = loc['LongLats'].str.split(',', n = 1, expand = True)
loc['Longitude'] = temp[0].astype(float)
loc['Latitude'] = temp[1].astype(float)

final = pd.concat([gigs, 
                   pd.DataFrame([x for x in gigs['All Artists'].str.split('/').values.tolist()])], axis=1, sort=False)
final = final.melt(id_vars=[c for c in gigs.columns], value_name='Fellow Artists', var_name='To_drop')
final = final.dropna(subset=['Fellow Artists'])
final['Fellow Artists'] = final.apply(lambda x: '' if x['Fellow Artists'].strip()==x['Artist'] else x['Fellow Artists'].strip(), axis=1)
final = pd.merge(final, home, how='inner', on='Artist')
final = pd.merge(final, loc, how='left', on='Location')
final.drop(['All Artists','To_drop','LongLats'],axis=1,inplace=True)
