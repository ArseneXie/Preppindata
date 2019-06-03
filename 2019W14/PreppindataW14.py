import pandas as pd

orders = pd.read_csv("E:\Cafe Orders by Product.csv")
meal_deal_price = 5

orders[['Price']] = orders[['Price']].fillna(value=1.5)
orders[['MemberID']] = orders[['MemberID']].fillna(value='0')

ticket = orders.groupby(['TicketID'], as_index=False).agg({'Price':'sum','Type':'nunique'})
ticket.rename(columns={'Price':'Total Ticket Price'}, inplace=True)
ticket = ticket[ticket['Type']==3]
ticket = ticket[['TicketID','Total Ticket Price']]
orders= orders.merge(ticket,on='TicketID', how='inner')

check = orders.groupby(['TicketID','Type']).size().to_frame(name='Type Count')
check = (check
         .join(orders.groupby(['TicketID','Type']).agg({'Price':'mean'})).rename(columns={'Price': 'TypeAvgPrice'})
         .join(orders.groupby(['TicketID','Type']).agg({'MemberID':'first'}))
         .join(orders.groupby(['TicketID','Type']).agg({'Total Ticket Price':'first'}))
         .reset_index()
         )
check['Meal Deal Count'] = check['Type Count'].groupby(check['TicketID']).transform('min')
check['Meal Deal Earning'] = check['Meal Deal Count']*meal_deal_price
check['Excess Earning'] = (check['Type Count']-check['Meal Deal Count'])*check['TypeAvgPrice']

final = check.groupby(['TicketID'], as_index=False).agg({'MemberID':'first',
                     'Total Ticket Price':'first',
                     'Meal Deal Earning':'first',
                     'Excess Earning':'sum'})
final.rename(columns={'Meal Deal Earning':'Total Meal Deal Earnings',
                      'Excess Earning':'Total Excess'}, inplace=True)
final['Tickets Price Variance to Meal Deal Earnings'] = (
        final['Total Ticket Price'] - final['Total Meal Deal Earnings']-final['Total Excess'] 
        )
