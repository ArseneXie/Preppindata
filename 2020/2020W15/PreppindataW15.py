import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

xls = pd.ExcelFile("E:/Transactions.xlsx")
txn = pd.read_excel(xls,sheet_name=0)
items = [list(map(str.strip, x)) for x in txn['Items'].str.split(',').values.tolist()]

te = TransactionEncoder()
te_ary = te.fit(items).transform(items)
df = pd.DataFrame(te_ary, columns=te.columns_)

support = apriori(df, min_support=0.01, use_colnames=True)
rules = association_rules(support, metric='lift', min_threshold=0.01)

rules['LHS Len'] = rules['antecedents'].apply(lambda x: len(x))
rules['RHS Len'] = rules['consequents'].apply(lambda x: len(x))
final = rules[(rules['LHS Len']==1) & (rules['RHS Len']==1)].copy()
final['antecedents'] = rules['antecedents'].apply(lambda x: list(x)[0])
final['consequents'] = rules['consequents'].apply(lambda x: list(x)[0])
final = final.rename(columns = {'antecedents':'LHS Item', 'consequents':'RHS Item',
                                'antecedent support':'LHS Support', 'consequent support':'RHS Support'})
final['Association Rule'] = final['LHS Item']+' --> '+final['RHS Item']
final = final[['Association Rule','LHS Item', 'RHS Item', 'LHS Support', 'RHS Support','confidence', 'lift']]
