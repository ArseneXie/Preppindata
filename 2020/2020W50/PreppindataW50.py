import pandas as pd
import re

xlsx = pd.ExcelFile("F:/Data/Secret Santa.xlsx")

final = pd.read_excel(xlsx,sheet_name=0)
final['Email'] = final['Email'].apply(lambda x: re.sub('(.*)@([a-z]+).([a-z]+)','\\1@\\2.\\3',x))
final['Secret Santee'] = (final.sort_values(by=['Secret Santa'], ascending=True)['Secret Santa'].shift(-1, fill_value=min(final['Secret Santa'])))
final['Email Subject'] = 'Secret Santa🤫🎅'
final['Email Body'] = final['Secret Santa']+', the results are in, your secret santee is: '+final['Secret Santee']+'. Good luck finding a great gift!'
final = final[['Email', 'Email Subject', 'Email Body']]
