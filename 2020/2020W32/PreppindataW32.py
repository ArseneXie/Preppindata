import pandas as pd

xlsx = pd.ExcelFile("F:/Data/Copy Down Data Challenge.xlsx")
final = pd.read_excel(xlsx,sheet_name=0)   
final['Store Manager'] = final['Store Manager'].ffill()
