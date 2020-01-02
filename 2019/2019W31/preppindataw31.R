library(readxl)
library(dplyr)
library(tidyr)
library(stringr)
library(lubridate)

order <- read_excel("E:/PD wk 31 input.xlsx", 
                            sheet = "Northern Customer Orders", 
                     col_types = c("numeric", "date", "text", "text", "text")) %>%
  mutate_at(vars('Status'), ~str_to_title(.)) %>%
  spread(`Status`,`Date`) %>%
  mutate('Time to Send' = time_length(`Sent`-`Purchased`, 'day'),
         'Time to Review from Sending Order' = time_length(`Reviewed`-`Sent`, 'day'),
         'Order Not Sent' = ifelse(is.na(`Sent`),'Not Sent','Sent'))

ans1 <- order %>%
  group_by(`Customer`) %>%
  summarise('Avg Time to Send' = mean(`Time to Send`))

ans2 <- order %>%
  group_by(`Customer`) %>%
  summarise('Time to Review from Sending Order' = mean(`Time to Review from Sending Order`,na.rm=TRUE)) %>%
  drop_na()

ans3 <- order %>%
  filter(`Order Not Sent`=='Not Sent') %>%
  select(c('City','Order Not Sent','Purchased','Sent','Order','Customer'))
  
ans4 <- order %>%
  group_by(`City`) %>%
  summarise('Orders per City'= n(),
         'Time To Send KPI'= sum(`Time to Send`<=3,na.rm=TRUE),
         '% Orders Meeting 3 Day KPI' = `Time To Send KPI`/`Orders per City`*100)

View(ans1)
View(ans2)
View(ans3)
View(ans4)