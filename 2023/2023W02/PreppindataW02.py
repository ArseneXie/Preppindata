import pandas as pd

transaction = pd.read_csv(r'C:/Data/PreppinData/Transactions.csv')
swift = pd.read_csv(r'C:/Data/PreppinData/Swift Codes.csv')

country_code = {'UK':'GB'}
final = pd.merge(transaction, swift, on='Bank')
final['IBAN'] = country_code['UK'] + final['Check Digits'] + final['SWIFT code'] \
    + final['Sort Code'].str.replace('-','') + final['Account Number'].astype(str)
final = final[['Transaction ID', 'IBAN']].copy()
