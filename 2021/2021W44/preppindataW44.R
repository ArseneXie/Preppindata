library(readxl)
library(dplyr)
library(tidyr)

final <- read_excel("C:/Data/PreppinData/Carl's 2021 cycling.xlsx") %>%
  mutate('Measure' = if_else(`Measure`=='km', 'Outdoors', 'Turbo Trainer'),
         'Date' = as.Date(`Date`)) %>%
  group_by(`Date`) %>%
  mutate('Activity per day' = n()) %>%
  pivot_wider(id_cols = c('Date', 'Activity per day'), names_from = 'Measure', values_from = 'Value', values_fn = sum) %>%
  ungroup() %>%
  complete(`Date` = seq.Date(min(`Date`), max(`Date`), by='day')) %>%
  replace(is.na(.), 0)

View(final)
