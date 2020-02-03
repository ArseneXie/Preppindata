import pandas as pd
import re

final = pd.read_csv(r'E:/PD 2020 Wk 5 Input.csv')
final['HTf'] = final['HTf'].apply(lambda x: None if re.search('(\D)',x) else x)
final = final.dropna(subset=['HTf'])[['Diff','Venue']]
final['Rank'] = final['Diff'].rank(ascending=False, method='min').astype(int)
final = final.groupby('Venue',as_index=False).agg({'Diff':[('Number of Games','count')],
                                                'Rank':[('Best Rank (Standard Competition)','min'),
                                                        ('Worst Rank (Standard Competition)','max'),
                                                        ('Avg Rank (Standard Competition)','mean')]})
final.columns = [col[1] if col[1] else col[0] for col in final.columns.values]
