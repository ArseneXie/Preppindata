library(dplyr)
library(tidyr)
library(readr)

orders <- read_csv("E:/Cafe Orders by Product.csv",
                  col_types = cols(TicketID = col_character(),
                                   MemberID = col_character())) %>%
  mutate_at(vars('MemberID'), ~replace_na(., '0')) %>%
  mutate_at(vars('Price'), ~replace_na(., 1.5)) 

final <- orders %>%
  group_by(`TicketID`) %>%
  mutate('Total Ticket Price' = sum(`Price`),
         'Count Type'= n_distinct(`Type`)) %>%
  filter(`Count Type`==3) %>%
  group_by(`TicketID`,`Type`) %>%
  summarise('Avg Type Price' = mean(`Price`),
            'Count Meal'= n(),
            'MemberID' = first(`MemberID`),
            'Total Ticket Price' = first(`Total Ticket Price`)) %>%
  group_by(`TicketID`) %>%
  mutate('Meal Deal Count' = min(`Count Meal`),
         'Excess Count' = `Count Meal` - min(`Count Meal`)) %>%
  summarise('MemberID' = first(`MemberID`),
            'Total Ticket Price' = first(`Total Ticket Price`),
            'Meal Deal Earnings' = 5*first(`Meal Deal Count`),
            'Total Excess' = sum(`Excess Count`*`Avg Type Price`)) %>%
  mutate('Tickets Price Variance to Meal Deal Earnings'=`Total Ticket Price`-`Meal Deal Earnings`-`Total Excess`) 

View(final)
