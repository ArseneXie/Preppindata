library(readxl)
library(dplyr)
library(tidyr)
library(purrr)
library(lubridate)

input <- "F:/Data/PD 2021 Wk 4 Input.xlsx"
final <- input %>%
  excel_sheets() %>% .[grepl('[^Targets]',.)] %>%
  set_names() %>%
  map_df(
    ~ read_excel(path = input, sheet = .x,),
    .id = 'Store') %>%
  mutate('Quarter' = quarter(`Date`)) %>%
  select(-'Date') %>%
  pivot_longer(cols=-c('Quarter','Store'), names_to='Customer Product', values_to = 'Products Sold') %>%
  group_by(`Quarter`,`Store`) %>%
  summarise('Products Sold' = sum(`Products Sold`), .groups = 'drop') %>%
  merge(.,read_excel(path = input, sheet = 'Targets'), by=c('Quarter','Store')) %>%
  group_by(`Quarter`) %>%
  mutate('Variance to Target' = `Products Sold` - `Target`,
         'Rank' = rank(desc(`Variance to Target`))) %>%
  arrange(`Quarter`,`Rank`) %>%
  select(c('Quarter', 'Rank', 'Store', 'Products Sold', 'Target', 'Variance to Target'))

View(final)
