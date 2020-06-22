import pandas as pd

xlsx = pd.ExcelFile("F:/Data/Roman Numerals.xlsx")
num = pd.read_excel(xlsx,'Number')   
roman = pd.read_excel(xlsx,'Roman Numerals')

final = pd.DataFrame(list(num['Number'][0]))
final.columns = ['Roman Numeral']
final['Number'] = num['Number'][0]
final = final.merge(roman, on='Roman Numeral')
final['Next Equivalent'] = final['Numeric Equivalent'].shift(-1).fillna(0)
# final[['Next Equivalent']] = final[['Next Equivalent']].fillna(0)
final['Numeric Equivalent'] = final.apply(lambda x: x['Numeric Equivalent'] if x['Numeric Equivalent']>=x['Next Equivalent']
                                          else x['Numeric Equivalent']*-1, axis=1)
final = final.groupby('Number', as_index=False).agg({'Numeric Equivalent':'sum'})
