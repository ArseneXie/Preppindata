import pandas as pd

df = pd.read_csv("F:/Data/2020W21 Input.csv")

df['Group'] = df['Company'].apply(lambda x: 'C&BSCo' if x=='Chin & Beard Suds Co' else 'Rest of Market')

finalA = ((df.groupby(['Company','Month']).agg({'Sales':'sum'}).rename(columns={'Sales': 'CM Total'}))
          .join(df.groupby(['Month']).agg({'Sales':'sum'})).rename(columns={'Sales': 'Mon Total'}).reset_index())
finalA = finalA.melt(id_vars=['Company','Month'],value_name='R2CVal', var_name='Measure Name')
finalA['R2CCol'] = finalA['Month']+' '+finalA['Measure Name']
finalA['R2CVal'] = round(finalA['R2CVal'])
finalA = finalA.pivot_table(index=['Company'],columns='R2CCol', values='R2CVal', aggfunc=max)
finalA.reset_index(inplace=True)
finalA['Growth'] = finalA.apply(lambda x: '{0:.2f}%'.format((x['April CM Total']-x['March CM Total'])/x['March CM Total']*100),axis=1)
finalA['April Market Share'] = finalA.apply(lambda x: x['April CM Total']/x['April Mon Total']*100,axis=1)
finalA['Bps Change'] = finalA.apply(lambda x: (x['April CM Total']/x['April Mon Total']-
                                               x['March CM Total']/x['March Mon Total'])/0.0001,axis=1)
finalA = finalA[['Company', 'Growth','April Market Share', 'Bps Change']].copy()

finalB = ((df.groupby(['Soap Scent','Group','Month']).agg({'Sales':'sum'}).rename(columns={'Sales': 'SGM Total'}))
          .join(df.groupby(['Group','Month']).agg({'Sales':'sum'})).rename(columns={'Sales': 'GM Total'}).reset_index())
finalB = finalB.melt(id_vars=['Soap Scent','Group','Month'],value_name='R2CVal', var_name='Measure Name')
finalB['R2CCol'] = finalB['Month']+' '+finalB['Measure Name']
finalB['R2CVal'] = round(finalB['R2CVal'])
finalB = finalB.pivot_table(index=['Soap Scent','Group'],columns='R2CCol', values='R2CVal', aggfunc=max)
finalB.reset_index(inplace=True)
finalB['R2CVal'] = finalB.apply(lambda x: (x['April SGM Total']-x['March SGM Total'])/x['March GM Total']*100,axis=1)
finalB['R2CCol'] = finalB['Group']+' Contribution to Growth'
finalB = finalB.pivot_table(index=['Soap Scent'],columns='R2CCol', values='R2CVal', aggfunc=max)
finalB.reset_index(inplace=True)
finalB['Outperformance'] = finalB['C&BSCo Contribution to Growth']-finalB['Rest of Market Contribution to Growth']
