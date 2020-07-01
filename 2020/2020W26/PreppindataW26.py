import pandas as pd

xlsx = pd.ExcelFile("F:/Data/Matching.xlsx")
sint = pd.read_excel(xlsx,'Internal Data')   
s3rd = pd.read_excel(xlsx,'3rd Party Data')

join_by_id = pd.merge(sint, s3rd, how = 'outer', left_on = ['ID','Scent'], right_on = ['3rd Party ID','Scent'], indicator='Status')
match_id = join_by_id[join_by_id['Status']=='both'].replace({'Status':{'both':'Matched'}})

join_by_scent = pd.merge(join_by_id[join_by_id['Status']=='left_only'][sint.columns], 
                         join_by_id[join_by_id['Status']=='right_only'][s3rd.columns], on = 'Scent')
join_by_scent['Diff'] = abs(join_by_scent['Sales'] - join_by_scent['3rd Party Sales'])
match_scent = join_by_scent.loc[join_by_scent.groupby('3rd Party ID')['Diff'].idxmin()]
match_scent = match_scent.loc[match_scent.groupby('ID')['Diff'].idxmin()].drop('Diff', axis=1)
match_scent['Status'] = 'Matched on Scent'

final = pd.concat([match_id, match_scent])

unmatch_int = sint[sint['ID'].isin(set(sint['ID']).difference(final['ID']))].copy()
unmatch_int['Status'] = 'Unmatched - Internal'
unmatch_3rd = s3rd[s3rd['3rd Party ID'].isin(set(s3rd['3rd Party ID']).difference(final['3rd Party ID']))].copy()
unmatch_3rd['Status'] = 'Unmatched - 3rd Party'

final = pd.concat([final, unmatch_int, unmatch_3rd]).reset_index(drop=True)
final = final[['Status','ID', '3rd Party ID', 'Scent', 'Sales', '3rd Party Sales']]
