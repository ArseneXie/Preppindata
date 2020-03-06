import pandas as pd
import itertools

xls = pd.ExcelFile("E:/PD 2020 Wk 10 Input.xlsx")
df = pd.read_excel(xls,sheet_name=0)
candidate = pd.DataFrame(list(itertools.product(
    df['Title'].tolist(), df['LastName'].tolist(), df['Product'].tolist(), df['Priority'].tolist())))
candidate.columns  = df.columns 

candidate['Pass'] = candidate.apply(lambda x: not(x['Title'][0:1]!=x['LastName'][0:1] and x['Priority']==1), axis=1)

candidate['Pass'] = candidate.apply(lambda x: not((x['LastName']=='Bevens' or x['LastName']=='Dimmadome') and
                                                  (x['Product']=='Chamomile Bar' or x['Product']=='Hibiscus Soap-on-a-Rope')) 
                                    if x['Pass'] else False, axis=1)

candidate['Pass'] = candidate.apply(lambda x: not((x['Title']=='Sergeant' and x['Product']=='Lemon Gel') and
                                                  (x['Priority']!=1 and x['Priority']!=3)) if x['Pass'] else False, axis=1)

candidate['Pass'] = candidate.apply(lambda x: not(x['Title']=='Reverend'  and
                                                  (x['Product']=='Rose Bar' or x['Priority']==2)) if x['Pass'] else False, axis=1)

candidate['Pass'] = candidate.apply(lambda x: not(x['Title']=='Sergeant'  and
                                                  (x['Product']!='Hibiscus Soap-on-a-Rope' and x['Priority']!=4)) if x['Pass'] else False, axis=1)

candidate['Pass'] = candidate.apply(lambda x: not((x['Title']!='Reverend' and x['LastName']=='Dimmadome') or
                                                  (x['Title']=='Baroness' and x['Product']=='Hibiscus Soap-on-a-Rope')) if x['Pass'] else False, axis=1)

candidate = candidate[candidate['Pass']].copy()

title = list(itertools.permutations(df['Title'].tolist(), 4))
lastname = list(itertools.permutations(df['LastName'].tolist(), 4))
product = list(itertools.permutations(df['Product'].tolist(), 4))


test = 'Arsene'
test[0:1]



title = pd.DataFrame(list(itertools.permutations(df['Title'].tolist(), 4)))
lastname = pd.DataFrame(list(itertools.permutations(df['LastName'].tolist(), 4)))
product = pd.DataFrame(list(itertools.permutations(df['Product'].tolist(), 4)))


from itertools import groupby

x = [(0, 'Add:'), (1, 'Net'), (2, 'Profit'), (4, 'Less:'), (5, 'Dep')]
for _, group in groupby(enumerate(x), lambda a:a[1][0] - a[0]):
    words = [text for _, (_,text) in group] # extract words from data structure
    print(' '.join(words))


result = pd.read_csv(r'E:/PD 2020 Wk 9 Input - Sheet1.csv', dtype=object)
result = result[~result['Poll'].str.contains('Average')]
result['Sample Type'] = result['Sample'].apply(lambda x: 'Registered Voter' if re.search('RV',x) else 'Likely Voter' if re.search('LV',x) else 'Unknown')

result['End Date'] = result['Date'].apply(lambda x: dt.strptime(re.search(r'(\d+/\d+$)',x).group(1),'%m/%d').date())
result['End Date'] = result['End Date'].apply(lambda x: x.replace(year=(2019 if x.month>10 else 2020)))
cols = result.columns.drop(['Poll','Sample Type','End Date'])
result[cols] = result[cols].apply(pd.to_numeric, errors='coerce')
result = result.drop(['Sample','Date'], axis=1).dropna()

final = result.melt(id_vars=['Poll','Sample Type','End Date'],var_name='Candidate',value_name='Poll Results')
final['Rank'] = final.groupby(['Poll','Sample Type','End Date'], as_index=False)['Poll Results'].rank(ascending=False, method='max').astype(int)
final['Spread'] = final.apply(lambda x: x['Poll Results']*(1 if x['Rank']==1 else -1 if x['Rank']==2 else 0), axis=1)
final['Spread from 1st to 2nd Place'] = final['Spread'].groupby([final['Poll'],final['Sample Type'],final['End Date']]).transform('sum')
final = final.drop('Spread', axis=1).sort_values(['End Date','Poll','Sample Type','Rank'])
