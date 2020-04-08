import pandas as pd
import re
from sklearn.preprocessing import minmax_scale

final = pd.read_csv(r'E:/PD Week 14 Input.csv',dtype=str)
for col in [c for c in final.columns if re.search('(\_)',c)]:
    final[col] = pd.to_numeric(final[col], errors='coerce')
final = final.dropna()
final['Species Count'] = final['Code'].groupby(final['Species']).transform('count')
final = final[final['Species Count']>=10].drop(['Code', 'Family', 'Sex', 'Location', 'Species Count'], axis=1).copy()
final = final.melt(id_vars = 'Species', value_name = 'Value', var_name = 'Trait')
final['Species'] = final['Species'].str.replace('_',' ')
final['Trait'] = final['Trait'].str.replace('_',' ')
final = final.groupby(['Species','Trait'], as_index=False).agg({'Value':'mean'})
final['Max Value'] = final['Value'].groupby(final['Trait']).transform('max')
final['Min Value'] = final['Value'].groupby(final['Trait']).transform('min')
final['Normalised Value'] = (final['Value'] - final['Min Value']) / (final['Max Value'] - final['Min Value'])

# Alternative method: Calculate with sklearn.preprocessing.minmax_scale
final['Normalised Value Alt'] = final.groupby('Trait')['Value'].transform(lambda x: minmax_scale(x))
