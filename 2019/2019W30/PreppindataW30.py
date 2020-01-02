import pandas as pd
import re
import string

tweet = pd.read_excel(pd.ExcelFile(r"E:\@serpsswimclub_user_tweets.xlsx"),"tweets")
tweet = tweet[['Tweet Id','Text', 'Created At']].copy()

tweet['Water-TempF'] = tweet['Text'].apply(lambda x: re.search('(?<=Water\s-\s)(-*\d+\.*\d*)', x).group(1) \
     if re.search('(?<=Water\s-\s)-*\d+\.*\d*', x) else None)
tweet['Water-TempC'] = tweet['Text'].apply(lambda x: re.search('(-*\d+\.*\d*)(?=C;)', x).group(1) \
     if re.search('-*\d+\.*\d*(?=C;)', x) else None)
tweet['Air-TempF'] = tweet['Text'].apply(lambda x: re.search('(?<=Air\s-\s)(-*\d+\.*\d*)', x).group(1) \
     if re.search('(?<=Air\s-\s)-*\d+\.*\d*', x) else None)
tweet['Air-TempC'] = tweet['Text'].apply(lambda x: re.search('(-*\d+\.*\d*)(?=C\.)', x).group(1) \
     if re.search('-*\d+\.*\d*(?=C\.)', x) else None)
tweet['Comment'] = tweet['Text'].apply(lambda x: re.search('(?<=C\.)(.*)', x).group(1) \
     if re.search('(?<=C\.)(.*)', x) else None)
tweet.dropna(inplace=True)
tweet['CommentTemp'] = tweet['Comment'].apply(lambda x: re.sub(f'[{string.punctuation}]','', str(x).lower()))
tweet['CommentTemp'] = tweet['CommentTemp'].str.replace('\\', '')
final = tweet.reset_index(drop=True)

commonWord = pd.read_excel(pd.ExcelFile(r"E:\Common English Words.xlsx"),"Sheet1")

final = pd.concat([final, 
                   pd.DataFrame([[y for y in x \
                                if y not in commonWord['Word'].str.lower().tolist()]
                                for x in final['CommentTemp'].str.split().values.tolist()])], axis=1, sort=False)
final = final.melt(id_vars=[c for c in tweet.columns],
                          value_name='Comment Split', var_name='Col Name').dropna().drop('Col Name',axis=1)

final.drop(['Text','CommentTemp'], axis=1, inplace=True)
final = final.melt(id_vars=[c for c in final.columns if not re.match('.*Temp.$',c)],value_name='R2CVal', var_name='CateTemp')
final['R2CVal']=final['R2CVal'].astype('float')
temp = final['CateTemp'].str.split('-', n = 1, expand = True) 
final['Category'] = temp[0]
final['R2CCol'] = temp[1]
final.drop(['CateTemp'], axis=1, inplace=True)
final = final.pivot_table(index=[c for c in final.columns if not re.match('^R2C',c)],
                                columns='R2CCol', values='R2CVal', aggfunc=max)
final.reset_index(inplace=True)

final2 = final.copy()
final2['check'] = final2['Comment Split'].apply(lambda x: re.match('(^[a-z])', x))
final2.dropna(inplace=True)
print(len(final2.index))