import pandas as pd

final = pd.read_excel(pd.ExcelFile("F:/Data/Input - Anagrams.xlsx"),'Anagrams')  
final['Anagram?'] = final.apply(lambda x: sorted(list(x['Word 1'].lower()))==sorted(list(x['Word 2'].lower())), axis=1)
