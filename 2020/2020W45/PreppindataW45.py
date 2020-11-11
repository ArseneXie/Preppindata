import pandas as pd
import re

xlsx = pd.ExcelFile("F:/Data/Prep Air Ticket Sales.xlsx")

country_map = {cl[0]:cl[2] for cl in pd.read_excel(xlsx,'Airports').to_dict('split')['data']}

proj = pd.read_excel(xlsx,'2020 Projections').melt(id_vars='Country', value_name='Proj', var_name='ToDrop').dropna()
proj['QFactor'] = proj['Proj'].apply(lambda x: 100 + (-1 if x[0:1]=='M' else 1)*int(re.sub('\D','',x)))
proj= proj.groupby('Country', as_index=False).agg({'QFactor':'sum'})
proj_map = {cl[0]:(cl[1]+100)/100 for cl in proj.to_dict('split')['data']} 

temp = []
for sheet in [sh for sh in xlsx.sheet_names if re.match('.*Sales.*',sh)]:
    df = pd.read_excel(xlsx,sheet)
    df.insert(0,'Type','Target Value' if re.match('.*Target.*',sheet) else 'Value')
    temp.append(df)
final = pd.concat(temp).drop('Date',axis=1)
final = final.pivot_table(index = ['Origin', 'Destination'],
                          columns='Type',values='Value', aggfunc={'Value':'sum'}).reset_index(drop=False)
final['Origin Country'] = final['Origin'].apply(lambda x: country_map[x])
final['Destination Country'] = final['Destination'].apply(lambda x: country_map[x])
final['Factor'] = final['Destination Country'].apply(lambda x: proj_map[x])
final['Value'] = final.apply(lambda x: x['Value']*x['Factor'], axis=1)
final['Target Value'] = final.apply(lambda x: x['Target Value']*x['Factor'], axis=1)
final['Variance to Target'] = final['Value'] - final['Target Value'] 
final = final[['Origin', 'Origin Country', 'Destination', 'Destination Country', 'Value', 'Target Value', 'Variance to Target']]
