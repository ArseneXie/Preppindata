library(readxl)
library(dplyr)
library(lubridate)

trans <- read_excel("E:/PD - Week 13.xlsx", 
                    sheet = "Transactions", col_types = c("numeric", 
                                                          "date", "numeric", "numeric"))
customer <- read_excel("E:/PD - Week 13.xlsx", 
                       sheet = "Customer Look-up")

temp <- trans %>%
  merge(., customer, by='Account') %>%
  mutate('Days Below Zero balance' = if_else(`Balance`<0,1,0),
         'Days Beyond Max Credit' = if_else(`Balance`*-1>`Max Credit`,1,0),
         'Week date' = if_else(floor_date(`Date`, 'weeks')<floor_date(`Date`, 'year'),
                               floor_date(`Date`, 'year'),floor_date(`Date`, 'weeks')),
         'Month date' = floor_date(`Date`, 'month'),
         'Quarter date' = floor_date(`Date`, 'quarter'),
         'Week' = as.integer(strftime(`Date`,format = '%U'))+1,
         'Month' = month(`Date`),
         'Quarter' = quarter(`Date`))

weekly <- temp %>%
  group_by(`Account`,`Name`,`Week`,`Week date`) %>% 
  summarise('Weekly Avg Transaction'= mean(`Transaction`),
            'Weekly Avg Balance'= mean(`Balance`),
            'Days Below Zero balance' = sum(`Days Below Zero balance`),
            'Days Beyond Max Credit' = sum(`Days Beyond Max Credit`)) %>%
  rename('Date'='Week date')
  
  
monthly <- temp %>%
  group_by(`Account`,`Name`,`Month`,`Month date`) %>% 
  summarise('Monthly Avg Transaction'= mean(`Transaction`),
            'Monthly Avg Balance'= mean(`Balance`),
            'Days Below Zero balance' = sum(`Days Below Zero balance`),
            'Days Beyond Max Credit' = sum(`Days Beyond Max Credit`)) %>%
  rename('Date'='Month date')

quarterly <- temp %>%
  group_by(`Account`,`Name`,`Quarter`,`Quarter date`) %>% 
  summarise('Quarterly Avg Transaction'= mean(`Transaction`),
            'Quarterly Avg Balance'= mean(`Balance`),
            'Days Below Zero balance' = sum(`Days Below Zero balance`),
            'Days Beyond Max Credit' = sum(`Days Beyond Max Credit`)) %>%
  rename('Date'='Quarter date')