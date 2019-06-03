import pandas as pd

xls = pd.ExcelFile("E:\Week7Challenge.xlsx")

dept = pd.read_excel(xls,"Departure Details") 
allc = pd.read_excel(xls,"Allocation Details") 

dept["Departure ID"]=dept["Ship ID"].map(str)+dept["Departure Date"].apply(lambda x: x.strftime('-%d-%m-%Y'))
dept["Departure Date"] = dept["Departure Date"].dt.strftime('%d/%m/%Y')

temp = dept.merge(allc, on="Departure ID", how='inner')

aggr = {
    'Max Weight':'max',
    'Max Volume':'max',
    'Weight Allocated':'sum',
    'Volume Allocated':'sum'
}

final = temp.groupby(["Ship ID","Departure Date"], as_index=False).agg(aggr)
final["Weight Exceeded"] = final.apply(lambda x: x['Weight Allocated']>x['Max Weight'],axis=1)
final["Volume Exceeded"] = final.apply(lambda x: x['Volume Allocated']>x['Max Volume'],axis=1)


