import pandas as pd
import re

final = pd.read_csv(r"C:\Data\PreppinData\2022W18 Input.csv")
final = final.melt(id_vars='Region', var_name='Cols', value_name='Amount')
final['Bike Type'] = final['Cols'].apply(lambda x: re.search('^([^_]+)(?=_)', x).group(1))
final['Measure'] = final['Cols'].apply(lambda x: re.search('(?<=_)([^_]+)$', x).group(1))
final['Month'] = final['Cols'].apply(lambda x: pd.to_datetime(re.sub('.*([A-Za-z]{3})_(\d+).*', '20\\2-\\1-01', x), 
                                                              format='%Y-%b-%d').date())
final = final.drop('Cols', axis=1)
final = final.pivot_table(index=['Bike Type', 'Region', 'Month'], columns='Measure', values='Amount', aggfunc=sum).reset_index()
final = final[['Bike Type', 'Region', 'Month', 'Sales', 'Profit']]
