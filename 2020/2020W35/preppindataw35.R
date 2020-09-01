library(dplyr)
library(readxl)
library(tidyr)
library(zoo)

Sys.setlocale("LC_ALL","English")

final <- read_excel("F:/Data/Input Week 35.xlsx", sheet = 'No RowID') %>%
  drop_na(!!names(.[2])) %>%
  do(na.locf(.)) %>%
  group_by(`Store`) %>%
  mutate('Type' = case_when(row_number()==1 ~ 'Sales',
                            row_number()==2 ~ 'Target',
                            TRUE ~ 'Difference')) %>%
  pivot_longer(., cols=matches('Sales$'), names_to='Month', values_to='Value') %>%
  mutate('Month' = as.Date(paste(substring(`Month`,1,3),'01','2020'), format='%b %d %Y')) %>%
  pivot_wider(., names_from='Type', values_from='Value')

View(final)