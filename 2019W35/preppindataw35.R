library(readxl)
library(dplyr)
library(lubridate)

supply <- read_excel(path = "E:/PD Wk 35 Input.xlsx", 
                     sheet = "PD Wk 34 Output") %>%
  mutate('Supply Id' = row_number()) %>%
  group_by(`Product`,`Scent`) %>%
  arrange(`Date`) %>%
  mutate('Running Supply To' = cumsum(`Quantity`),
         'Running Supply From' = `Running Supply To`-`Quantity`)

demand <- read_excel(path = "E:/PD Wk 35 Input.xlsx", 
                     sheet = "Store Orders") %>%
  mutate('Demand Id' = row_number()) %>%
  group_by(`Product`,`Scent`) %>%
  arrange(`Date Required`) %>%
  mutate('Running Demand To' = cumsum(`Quantity Requested`),
         'Running Demand From' = `Running Demand To`-`Quantity Requested`)

allocate <- merge(supply, demand, on = c('Product','Scent')) %>%
  filter((`Running Demand To`>=`Running Supply From` & `Running Demand To`<=`Running Supply To`) | 
           (`Running Supply To`>=`Running Demand From` & `Running Supply To`<=`Running Demand To`))

surplus <- anti_join(supply, allocate, by = 'Supply Id') %>%
  group_by(`Supplier`,`Product`,`Scent`) %>%
  summarise('Quantity' = sum(`Quantity`))

fulfill <- allocate %>%
  group_by(`Store`,`Product`,`Scent`,`Supplier`,`Quantity Requested`,`Date Required`) %>%
  summarise('Date Fulfilled' = max(max(`Date`),`Date Required`)) %>%
  mutate('Days Request Delayed' = time_length(`Date Fulfilled`-`Date Required`,'day'),
         'Stock Ready?' = (`Date Fulfilled`== `Date Required`))
 
View(surplus)  
View(fulfill)  