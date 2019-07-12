import pandas as pd
from datetime import datetime

sales = pd.read_csv("E:\PD Wk 22 Input.csv")
sales['Date']=sales['Date'].apply(lambda x: datetime.strptime(x, "%d/%m/%Y").date())
sales['Moving Avg Sales'] = sales.rolling(7)['Sales'].mean()
sales.drop(['Sales'],axis=1,inplace = True)
