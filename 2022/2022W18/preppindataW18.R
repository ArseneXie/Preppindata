library(readr)
library(dplyr)
library(tidyr)

Sys.setlocale("LC_ALL","English")

final <- read_csv("C:/Data/PreppinData/2022W18 Input.csv") %>%
  pivot_longer(cols = -'Region', names_to = c('Bike Type', 'Mth', 'Yr', 'Measure'), 
               names_pattern='(\\w+)___(\\w+)_(\\d+)+___(\\w+)', values_to = 'Amount') %>%
  mutate('Month' = as.Date(paste0('20',`Yr`,'-',`Mth`,'-01'), format='%Y-%b-%d')) %>%
  pivot_wider(id_cols = -'Measure', names_from='Measure', values_from='Amount', values_fn=sum) %>%
  select(c('Bike Type', 'Region', 'Month', 'Sales', 'Profit'))

View(final)
