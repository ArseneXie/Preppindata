import pandas as pd

supply = pd.read_excel(r'E:\PD Wk 35 Input.xlsx','PD Wk 34 Output')
supply['Supply Id'] =  supply.index+1
supply['Running Supply To'] =  supply.sort_values('Date').groupby(['Product','Scent'])['Quantity'].cumsum()
supply['Running Supply From'] =  supply['Running Supply To'] - supply['Quantity']

demand = pd.read_excel(r'E:\PD Wk 35 Input.xlsx','Store Orders')
demand['Demand Id'] =  demand.index+1 
demand['Running Demand To'] =  demand.sort_values('Date Required').groupby(['Product','Scent'])['Quantity Requested'].cumsum()
demand['Running Demand From'] =  demand['Running Demand To'] - demand['Quantity Requested']

allocate = pd.merge(supply,demand,on=['Product','Scent'],how='inner')
allocate = allocate.query('(`Running Demand To`>=`Running Supply From` and `Running Demand To`<=`Running Supply To`) \
                          or (`Running Supply To`>=`Running Demand From` and `Running Supply To`<=`Running Demand To`)')
allocate['Allocated Quantity'] =  allocate.apply(lambda x: 
    min(x['Running Supply To'],x['Running Demand To'])-max(x['Running Supply From'],x['Running Demand From']) , axis=1 )
    
surplus = supply[~supply['Supply Id'].isin(allocate['Supply Id'])]    
surplus = surplus.groupby(['Supplier','Product','Scent'],as_index=False).agg({'Quantity':'sum'})

fulfill = allocate.groupby(['Store','Product','Scent','Supplier','Quantity Requested','Date Required'],as_index=False).agg({
   'Date':'max'}).rename(columns={'Date':'Date Fulfilled'})
fulfill['Date Required'] = fulfill['Date Required'].apply(lambda x: x.date()) 
fulfill['Date Fulfilled'] = fulfill['Date Fulfilled'].apply(lambda x: x.date()) 
fulfill['Days Request Delayed'] = fulfill.apply(lambda x: max((x['Date Fulfilled']-x['Date Required']).days,0) , axis=1)
fulfill['Stock Ready?'] = fulfill['Days Request Delayed'].apply(lambda x: x==0)
fulfill['Date Fulfilled'] = fulfill.apply(lambda x: x['Date Required'] if x['Stock Ready?'] else x['Date Fulfilled'] , axis=1)
