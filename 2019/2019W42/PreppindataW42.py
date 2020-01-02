import pandas as pd
import geonamescache

gc = geonamescache.GeonamesCache()
countries = gc.get_countries_by_names()

xls = pd.ExcelFile("E:/PD Wk 42 Input.xlsx")
instance = pd.read_excel(xls,'Sheet1')
currency = pd.read_excel(xls,'Currency Conversion')

temp = instance['Location'].str.split(',', n = 1, expand = True) 
instance['City'] = temp[0].str.strip()
instance['Country'] = temp[1].str.strip()
instance['Check City'] = instance['City'].apply(lambda x: len(gc.get_cities_by_name(x)) + len(gc.get_cities_by_name(x+' City')) )
instance['Check Country'] = instance['Country'].apply(lambda x: 0 if countries.get(x,0)==0 else 1)
instance = instance.query('`Check City`>0 & `Check Country`>0').copy()

temp = instance['Store Potential Sales'].str.split(' ', n = 1, expand = True) 
instance['Store Potential Sales'] = temp[0].str.strip().astype('int64')
instance['Currency'] = temp[1].str.strip()

temp = instance['Store Cost'].str.split(' ', n = 1, expand = True) 
instance['Store Cost'] = temp[0].str.strip().astype('int64')

final = pd.merge(instance,currency,how='inner', on='Currency')[['City', 'Country', 
                'Potential Store Location', 'Store Potential Sales', 'Store Cost','Currency', 'Value in USD']]
final = final.query('`Store Potential Sales`>= `Store Cost`').copy()
final.rename(columns={'Potential Store Location':'Zip Code'}, inplace=True)
final = final.iloc[final.reset_index().groupby('Zip Code')['Store Potential Sales'].idxmax()]
