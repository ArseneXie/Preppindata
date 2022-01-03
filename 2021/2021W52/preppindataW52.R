library(readxl)
library(dplyr)
library(fuzzyjoin)

xlsx <- "C:/Data/PreppinData/PD 2021 Wk 52 Input.xlsx"

final <- read_excel(xlsx, 'Complaints') %>%
  group_by(`Name`) %>%
  mutate('Complaints per person' = n()) %>%
  regex_left_join(read_excel(xlsx, 'Department Responsbile') %>%
                     mutate('Keyword' = tolower(`Keyword`),
                            'Pattern'=paste0('.*',tolower(`Keyword`),'.*')),
                   by = c(`Complaint`='Pattern')) %>%
  mutate_at(vars('Keyword'), ~replace_na(., 'other')) %>%
  mutate_at(vars('Department'), ~replace_na(., 'Unknown')) %>%
  group_by(`Complaint`,`Department`, `Name`, `Complaints per person`) %>%
  summarise('Complaint causes' = toString(sort(unique(`Keyword`))), .groups='drop') %>%
  select(c('Complaint', 'Complaint causes', 'Department', 'Name', 'Complaints per person'))
  
View(final)
