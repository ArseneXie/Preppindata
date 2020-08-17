library(dplyr)
library(readxl)
library(tidyr)
library(stringr)

xlsx <- "F:/Data/Attendee List.xlsx"

finalA <- read_excel(xlsx, sheet = 'Attendee List') %>%
  mutate('Currency' = case_when(`Country`=='United States' ~ 'USD',
                                `Country`=='Canada' ~ 'CAD',
                                `Country`=='Mexico' ~ 'MXN',
                                `Country`=='United Kingdom' ~ 'GBP',
                                TRUE ~ 'EUR'),
         'Lower Company' = tolower(str_extract(`Email`,'(?<=@)([^\\.]*)(?=\\.)'))) %>%
  merge(read_excel(xlsx, sheet = 'Account Manager') %>%
          transform(.,'Order'=as.numeric(factor(`Account Manager`))) %>%
          rename('Company Name' = !!names(.[1]), 'Account Manager' = !!names(.[2])) %>%
          mutate('Lower Company' = tolower(`Company Name`)), by='Lower Company') %>%
  merge(read_excel(xlsx, sheet = 'Exchange Rates') %>%
          mutate('Currency' = str_extract(`Currency`,'^\\w{3}')) %>%
          select(-'GBP') %>%
          rbind(., data.frame('Currency'='GBP', 'Rate'=1)), by='Currency') %>%
  mutate('Ticket Price Local' = `Ticket Price (¢G)`*`Rate`) %>%
  select(c('First Name', 'Last Name', 'Email', 'Country', 'Refund Type',
           'Currency', 'Company Name', 'Account Manager', 'Order','Ticket Price Local'))
  
finalB <- finalA %>%
  group_by(`Country`,`Currency`) %>%
  summarize('Money Gain/Loss' = sum(`Ticket Price Local`*if_else(`Refund Type`=='Full Refund',-1,1)))
  
View(finalA)
View(finalB)