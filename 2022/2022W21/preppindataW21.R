library(readxl)
library(dplyr)
library(tidyr)
library(stringr)
library(purrr)
library(lubridate)

xlsx <- "C:/Data/PreppinData/2022W21 Input.xlsx"

metrics <-  xlsx %>%
  excel_sheets() %>%
  set_names() %>%
  map_df(
    ~ read_excel(path = xlsx, sheet = .x, skip = 3), .id = 'Shop')  %>%
  select(-starts_with('FY')) %>%
  fill(c('Department', 'Target'), .direction = 'down') %>%
  filter(`Department` %in% c('Orders', 'Returns', 'Complaints')) %>%
  filter(`Breakdown` %in% c('% Shipped in 3 days', '% Shipped in 5 days', 
                            '% Processed in 3 days', '% Processed in 5 days', '# Received')) %>%
  mutate('Breakdown' = str_replace_all(`Breakdown`, '(.)\\s(.+)', paste('\\1', `Department`, '\\2')),
         'Target' = as.numeric(sub('>', '', sub('%','e-2', `Target`)))) %>%
  select(-c('Department', 'Comments')) %>%
  pivot_longer(cols=-c('Shop', 'Target', 'Breakdown'), names_to='Date', values_to = 'Value',
               values_drop_na = TRUE, values_transform  = list(Value = as.numeric)) %>%
  mutate('Date' = as.Date(as.numeric(`Date`), origin = '1899-12-30'))
  
final <- rbind(metrics %>% select(c('Shop', 'Date', 'Breakdown', 'Value')), 
               metrics %>% select(c('Shop', 'Date', 'Breakdown', 'Target')) %>%
                 rename('Value' = 'Target') %>%
                 mutate('Breakdown' = paste('Target -', `Breakdown`))) %>%
  pivot_wider(id_cols=c('Shop', 'Date'), names_from='Breakdown', values_from='Value') %>%
  select(c('Shop', 'Date', 
           '% Orders Shipped in 3 days', 'Target - % Orders Shipped in 3 days',
           '% Orders Shipped in 5 days', 'Target - % Orders Shipped in 5 days',
           '% Returns Processed in 3 days', 'Target - % Returns Processed in 3 days',
           '% Returns Processed in 5 days', 'Target - % Returns Processed in 5 days',
           '# Complaints Received', 'Target - # Complaints Received'))
 
View(final)
