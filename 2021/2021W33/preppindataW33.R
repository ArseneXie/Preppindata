library(readxl)
library(dplyr)
library(lubridate)
library(purrr)

input <- "F:/Data/Allchains Weekly Orders.xlsx"

final <-  input %>%
  excel_sheets() %>% 
  set_names() %>%
  map_df(
    ~ read_excel(path = input, sheet = .x,),
    .id = 'Reporting Date') %>%
  group_by(`Orders`) %>%
  mutate('Reporting Date' = as.Date(`Reporting Date`, format = "%Y%m%d"),
         'Order Max Report Date' = max(`Reporting Date`),
         'Order Status' = if_else(`Reporting Date`==min(`Reporting Date`),'New Order', 'Unfulfilled Order')) %>%
  ungroup() %>%
  rbind(., filter(., `Reporting Date`==`Order Max Report Date` & `Reporting Date`<max(`Reporting Date`)) %>%
          mutate('Order Status' = 'Fulfilled',
                 'Reporting Date' = `Reporting Date` + weeks(1))) %>%
  select(c('Order Status', 'Orders', 'Sale Date', 'Reporting Date')) %>%
  arrange(`Orders`, `Reporting Date`)

View(final)
