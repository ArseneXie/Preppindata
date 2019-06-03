import pandas as pd

xls = pd.ExcelFile("E:\Week 8 Input.xlsx")
theft = pd.read_excel(xls,"Theft Audit") 
branch = pd.read_excel(xls,"Branch ID") 
theft["Type"] = theft["Type"].str.replace('^L.*','Liquid',regex=True)
theft["Type"] = theft["Type"].str.replace('.*Bar.*','Bar',regex=True)

temp = branch["Branch ID"].str.split(" - ", n = 1, expand = True) 
branch["Store ID"] = temp[0]
branch["Branch Name"] = temp[1]

final = theft.merge(branch, on="Store ID", how='inner')
final = final.pivot_table(index = ["Branch Name", "Crime Ref Number","Type"],
                          columns="Action",
                          values=["Date","Quantity"],
                          aggfunc={"Date":'max',"Quantity":'sum'})

final.columns=['_'.join(str(s).strip() for s in col if s) for col in final.columns]
final["Quantity_Stock Adjusted"].fillna(0,inplace = True)

final["Days to comp Adj"] = final.apply(lambda x: x["Date_Stock Adjusted"]-x["Date_Theft"],axis=1) 
final["Quantity Variance"] = final.apply(lambda x:  x["Quantity_Stock Adjusted"]+x["Quantity_Theft"],axis=1) 

final.rename(columns={'Date_Stock Adjusted':'Stock Adjusted',
                      'Date_Theft':'Theft',
                      'Quantity_Theft':'Stolen Volume'}, 
                 inplace=True)
final.drop("Quantity_Stock Adjusted",axis=1,inplace = True)
final.reset_index(inplace = True)

