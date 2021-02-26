import pandas as pd
import re

shopping = pd.read_excel(pd.ExcelFile("F:/Data/Shopping List and Ingredients.xlsx"),sheet_name='Shopping List')
df = pd.read_excel(pd.ExcelFile("F:/Data/Shopping List and Ingredients.xlsx"),sheet_name='Keywords')

keywd = [c.lower().strip() for c in  df['Animal Ingredients'][0].split(',')]+ ['e'+c.strip() for c in df['E Numbers'][0].split(',')]

shopping['check'] = shopping['Ingredients/Allergens'].apply(lambda x: re.sub('\W+',',',x.lower()).split(','))
shopping['Contains'] = shopping['check'].apply(lambda x: ', '.join(sorted(list(set(x) & set(keywd)))))

vegan_list = shopping[shopping['Contains']==''][['Product','Description']].reset_index(drop=True)
non_vegan_list = shopping[shopping['Contains']!=''][['Product','Description','Contains']].reset_index(drop=True)
