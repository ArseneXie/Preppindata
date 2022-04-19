import pandas as pd

sales = pd.read_csv(r"C:\Data\PreppinData\Pareto Input.csv")
sales = sales.groupby(['Customer ID', 'First Name', 'Surname'], as_index=False).agg({'Sales':'sum'})
sales['% of Total'] = sales['Sales']/sales['Sales'].sum()*100 
sales['Running % of Total Sales']=round(sales.sort_values('Sales', ascending=False)['% of Total'].cumsum(),2)

def gen_output(sales_df, pert_of_sales):
    df1 = sales_df[sales_df['Running % of Total Sales'] <= pert_of_sales].sort_values('Sales', ascending=False).copy()
    df1.to_csv(f'Pareto Output {pert_of_sales}%.csv', index=False)
    
    df2=pd.DataFrame([f'{round(len(df1)/len(sales_df)*100)}% of Customers account for {pert_of_sales}% of Sales'],
                     columns=['outcomes'])
    df2.to_csv(f'Pareto In Words {pert_of_sales}%.csv', index=False)
    return df1
    
final = gen_output(sales, 80)    
