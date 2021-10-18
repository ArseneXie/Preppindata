library(readr)
library(dplyr)
library(tidyr)
library(stringr)

final <- read_csv("C:/Data/PreppinData/Bike Painting Process - Painting Process.csv") %>%
  mutate('Datetime' = as.POSIXct(paste(`Date`, `Time`),format='%d/%m/%Y %H:%M:%S'),
         'Bike Type' = if_else(`Data Parameter`=='Bike Type', `Data Value`, NA_character_),
         'Batch Status' = if_else(`Data Parameter`=='Batch Status', `Data Value`, NA_character_),
         'Name of Process Stage' = if_else(`Data Parameter`=='Name of Process Stage', `Data Value`, NA_character_)) %>%
  group_by(`Batch No.`) %>%
  arrange(`Datetime`) %>%
  fill(`Bike Type`, `Batch Status`, `Name of Process Stage`) %>%
  filter((`Data Type`=='Process Data') & (`Data Parameter`!='Name of Process Stage')) %>%
  mutate('Actual' = if_else(str_detect(`Data Parameter`, '^(Actual)'), as.numeric(`Data Value`), NA_real_),
         'Target' = if_else(str_detect(`Data Parameter`, '^(Target)'), as.numeric(`Data Value`), NA_real_),
         'Data Parameter' = str_remove(`Data Parameter`,'^(\\w+\\s)')) %>%
  select(c('Batch No.', 'Bike Type', 'Batch Status', 'Name of Process Stage',
           'Data Parameter', 'Actual', 'Target', 'Datetime'))

View(final)
