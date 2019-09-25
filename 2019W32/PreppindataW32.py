import pandas as pd
import re

sales = pd.read_excel(pd.ExcelFile(r"E:\PD Wk 32 input.xlsx"),"Multiple Product Purchases",
                      dtype=str)

sales = pd.concat([sales, 
                   pd.DataFrame([map(str.strip, x) \
                                 for x in sales['Address'].str.split(',').values.tolist()])],
    axis=1, sort=False)
sales.rename(columns={0:'Property Number', 1:'Twon', 2:'Postal Code', 3:'Country'}, inplace=True)
sales['Property Number']=sales['Property Number'].apply(lambda x: int(re.sub('[^\d]','',x)))
sales['Prod-Sales-1']=sales.apply(lambda x: re.sub('-',' ',x['Product 1'])+'/'+x['Sales'], axis=1)
sales['Prod-Sales-2']=sales.apply(lambda x: re.sub('-',' ',x['Product 2'])+'/'+x['Sales.1'], axis=1)
sales.drop(['Address','Product 1','Sales','Product 2','Sales.1'], inplace=True, axis=1)
sales=sales.melt(id_vars=[c for c in sales.columns if not re.match('^Prod-Sales',c)],
                          value_name='ProdSales', var_name='ToDrop').drop('ToDrop', axis=1)
temp = sales['ProdSales'].str.split('/',n = 1, expand = True)
sales['Product'] = temp[0]
sales['Sales'] = temp[1]
sales = sales.astype({'Sales': int}).drop(['ProdSales'], axis=1)
