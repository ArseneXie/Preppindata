import pandas as pd
import os
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

os.chdir(r'E:/PD16/')
startdate = datetime(2019,5,24,0,0) + relativedelta(months=-6)

mergedata = []
for files in [f for f in os.listdir('.') if re.match('^Sales', f)]:
    dataset = pd.read_csv(files)
    dataset = dataset[pd.to_datetime(dataset['Order Date'])>=startdate]
    mergedata.append(dataset)    
sales_dtl = pd.concat(mergedata)   

sales_cus = sales_dtl.groupby('Email',as_index=False).agg({'Order Total':'sum'})

final = sales_cus.nlargest(int(len(sales_cus.index)*0.08), 'Order Total')
final = final.reset_index(drop=True)
final['Last 6 Months Rank'] = final.index+1
