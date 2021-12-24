import pandas as pd

salary = pd.read_csv("C:\\Data\\PreppinData\\PD 2021 Wk 49 Input - Input.csv", 
                     parse_dates=['Date'], date_parser=lambda x: pd.to_datetime(x, format='%d/%m/%Y'))
salary['Report Year'] = salary['Date'].dt.year
salary['Min Date'] = salary['Date'].groupby(salary['Name']).transform('min').dt.strftime('%b %Y')
salary['Max Date'] = salary['Date'].groupby(salary['Name']).transform('max').dt.strftime('%b %Y')
salary['Employment Range'] = salary['Min Date']+' to '+salary['Max Date']
salary['Tenure by End of Reporting Year'] = salary.sort_values('Date').groupby(['Name']).cumcount()+1
salary['Salary Paid'] = salary['Annual Salary']/12
salary['Yearly Bonus'] = salary['Sales']*0.05

salary = salary.groupby(['Name', 'Report Year'], as_index=False).agg({
    'Employment Range':'first', 'Tenure by End of Reporting Year':'max', 'Salary Paid':'sum', 'Yearly Bonus':'sum'})
salary['Salary Paid'] = round(salary['Salary Paid'],2)
salary['Total Paid'] = round(salary['Salary Paid']+salary['Yearly Bonus'])
salary = salary[['Name', 'Employment Range', 'Report Year', 
       'Tenure by End of Reporting Year', 'Salary Paid', 'Yearly Bonus', 'Total Paid']]
