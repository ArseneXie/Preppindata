import pandas as pd
import re

xlsx = {'Boys':pd.ExcelFile("F:/Data/2019boysnames.xlsx"), 'Girls':pd.ExcelFile("F:/Data/2019girlsnames.xlsx")}

temp = []
for gender,skip,nr in [('Boys',5,10),('Boys',19,10),('Boys',33,10),('Girls',5,10),('Girls',19,11),('Girls',34,12)]:
    df = pd.read_excel(xlsx[gender],sheet_names=1,skiprows=skip, nrows=nr,header=[0, 1]).dropna(axis=1, how='all')  
    df.columns = [col[0]+'-'+col[1] for col in df.columns.values]
    df = df.melt(id_vars = [c for c in df.columns if not re.search('Rank$',c)],value_name = 'Rank', var_name='Type1')
    df = df.melt(id_vars = [c for c in df.columns if not re.search('Name$',c)],value_name = 'Name', var_name='Type2')
    df['Keep'] = df.apply(lambda x: x['Type1'].split('-')[0]==x['Type2'].split('-')[0], axis=1)
    df = df[df['Keep']].melt(id_vars = [c for c in df.columns if not re.search('Count$',c)],value_name = 'Count', var_name='Type3')
    df['Keep'] = df.apply(lambda x: x['Type1'].split('-')[0]==x['Type3'].split('-')[0], axis=1)
    df['Gender'] = gender
    temp.append(df[df['Keep']])
final = pd.concat(temp).dropna()  
final['Month'] = final['Type1'].str.split('-', n = 1, expand = True)[0]
final = final.drop(['Type1','Type2','Type3','Keep'], axis=1)

output1 = final[['Gender', 'Month', 'Rank', 'Name', 'Count']]

output2 = final.groupby(['Gender','Name'], as_index=False).agg({'Count':'sum'})
output2['2019 Rank'] = output2.groupby('Gender')['Count'].rank(ascending=False).astype(int)
output2 = output2[output2['2019 Rank']<=10][['Gender', '2019 Rank', 'Name', 'Count']]
