library(readr)
library(dplyr)
library(tidyr)

final <- read_csv("F:/Data/PD 2021 Wk 31 Input.csv") %>%
  filter(`Status` != 'Return to Manufacturer') %>%
  select(c('Store', 'Item', 'Number of Items')) %>%
  group_by(`Store`) %>%
  mutate('Item sold per store' = sum(`Number of Items`)) %>%
  pivot_wider(id_cols=c('Store', 'Item sold per store'),  names_from='Item', values_from='Number of Items', values_fn = sum) %>%
  select(c('Store', 'Wheels', 'Tyres', 'Saddles', 'Brakes', 'Item sold per store'))

View(final)
