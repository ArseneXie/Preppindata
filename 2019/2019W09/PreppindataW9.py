import pandas as pd
import string

xls = pd.ExcelFile("H:\PD - Week 9 Complaints.xlsx")

complaint = pd.read_excel(xls,"Complaints") 
commonWord = pd.read_excel(xls,"Common English Words") 

complaint['tempstr']=complaint['Tweet'].str.replace('@C&BSudsCo','')
complaint['Tweet']=complaint['tempstr'].str.translate(str.maketrans(dict.fromkeys(string.punctuation)))
complaint['Tweet']=complaint['Tweet'].str.replace("’","")
complaint['word']=complaint['tempstr'].str.split(' ')

check=pd.DataFrame([[y for y in x \
                     if y.lower() not in commonWord['Word'].str.lower().tolist()] \
     for x in complaint['Tweet'].str.split().values.tolist() ])

final = pd.concat([complaint['Tweet'], check], axis=1, sort=False)
final = final.melt(id_vars=['Tweet'], value_name='Words')
final = final[['Words','Tweet']]
final = final.dropna()
