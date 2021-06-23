import pandas as pd
import re

xlsx = pd.ExcelFile("F:/Data/Answer Smash Input.xlsx")

names = pd.read_excel(xlsx,'Names')
questions = pd.read_excel(xlsx,'Questions')
category = pd.read_excel(xlsx,'Category')
smash = pd.read_excel(xlsx,'Answer Smash')

smash['dummy'] = 1 
names['dummy'] = 1 
temp = category['Category: Answer'].str.split(':', n = 1, expand = True) 
category['Category'] = temp[0].str.strip() 
category['Answer'] = temp[1].str.strip()
category = category.drop('Category: Answer', axis=1)

final = pd.merge(smash, names, on='dummy')
final['Check'] = final.apply(lambda x: 1 if re.search(x['Name'], x['Answer Smash']) else 0, axis=1)
final = final[final['Check']==1].copy()
final = final.merge(questions, on='Q No')
final = final.merge(category, on='Category')
final['Check'] = final.apply(lambda x: 1 if re.search(x['Answer'].lower(), x['Answer Smash'].lower()) else 0, axis=1)
final = final[final['Check']==1].copy()
final = final[['Q No', 'Name', 'Question', 'Answer', 'Answer Smash']].copy()
