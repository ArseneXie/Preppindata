import pandas as pd

xlsx = pd.ExcelFile("E:/2020W20 Input.xlsx")
decoder = pd.read_excel(xlsx,'Cipher').set_index('Cipher').T.to_dict('records')[0]
#encoder = pd.read_excel(xlsx,'Cipher').set_index('Alphabet').T.to_dict('records')[0]

cipher_text = pd.read_excel(xlsx,'Encrypted Message')['Encrypted Message'][0]
plain_text = ''.join([decoder.get(c,c) for c in list(cipher_text)])
print(plain_text)
