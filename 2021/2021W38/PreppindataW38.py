import pandas as pd

xlsx = pd.ExcelFile(r"F:\Data\Trend Input.xlsx")

timeline = pd.read_excel(xlsx,'Timeline', skiprows=2)
timeline['Week'] = timeline['Week'].dt.date
timeline = timeline.melt(id_vars='Week', value_name='Index', var_name='Search Term')
timeline['Search Term'] = timeline['Search Term'].replace('(:.*)','', regex = True)
timeline['Avg Index'] = round(timeline['Index'].groupby(timeline['Search Term']).transform('mean'),1)
timeline['Index Peak'] = timeline['Index'].groupby(timeline['Search Term']).transform('max')
timeline['Index Peak Week'] = timeline.apply(lambda x: x['Week'] if x['Index']==x['Index Peak'] else max(timeline['Week']), axis=1)
timeline['First Peak'] = timeline['Index Peak Week'].groupby(timeline['Search Term']).transform('min')
timeline['Year'] = timeline['Week'].apply(lambda x: x.year+1 if x.month>=9 else x.year)
timeline = timeline[timeline['Year']>=max(timeline['Year'])-1].copy()
timeline['YearMeasure'] = timeline['Year'].apply(lambda x: f'{str(x-1)}/{str(x)[2:]} avg index')
timeline = timeline.drop(['Week', 'Index Peak Week', 'Year'], axis=1)

country = pd.read_excel(xlsx,'Country Breakdown', skiprows=2).dropna()
country = country.melt(id_vars='Country', value_name='Percentage', var_name='Search Term')
country['Search Term'] = country['Search Term'].replace('(:.*)','', regex = True)
country = country.loc[country.reset_index().groupby(['Search Term'])['Percentage'].idxmax()][['Search Term','Country']]

final = timeline.pivot_table(index=[c for c in timeline.columns if c not in ['Index','YearMeasure']], 
                             columns='YearMeasure', values='Index', aggfunc='mean').reset_index()
final['Status'] = final.apply(lambda x: 'Still Trendy' if x['2020/21 avg index']>=x['2019/20 avg index'] else 'Lockdown Fad', axis=1)
final['2020/21 avg index'] = round(final['2020/21 avg index'],1)
final = final.merge(country, on='Search Term').rename(columns={'Country':'Country with highest percentage'})
final = final[['Search Term', 'Status', '2020/21 avg index', 'Avg Index', 'Index Peak', 'First Peak', 'Country with highest percentage']]
