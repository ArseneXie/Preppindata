library(readxl)
library(dplyr)
library(tidyr)

xlsx <- "C:/Data/PreppinData/Sales Department Input.xlsx"

final <-  read_excel(xlsx, 'October', col_types = c("numeric", "date", "text", "numeric", "numeric", "numeric", "text", "numeric")) %>%
  rename('Oct YTD Total' = names(.)[length(names(.))]) %>%
  bind_rows(., read_excel(xlsx, 'November', col_types = c("numeric", "date", "text", "numeric", "numeric", "numeric", "text"))) %>%
  fill(`Salesperson`, .direction = 'up') %>%
  group_by(`Salesperson`) %>%
  mutate('Oct YTD Total' = max(`Oct YTD Total`, na.rm = TRUE),
         'Month' = format(`Date`,'%m')) %>%
  filter(!is.na(`Date`)) %>%
  pivot_longer(cols=c('Road', 'Gravel', 'Mountain'), names_to = 'Bike Type', values_to = 'Sales') %>%
  group_by(`Salesperson`, `Month`) %>%
  mutate('Monthly Total' = sum(`Sales`),
         'YTD Total' = `Oct YTD Total` + if_else(`Month`==11, `Monthly Total`, 0)) %>%
  ungroup() %>%
  select(c('Salesperson', 'Date', 'Bike Type', 'Sales', 'YTD Total'))
  
View(final)
