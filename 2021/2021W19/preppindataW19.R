library(readxl)
library(dplyr)
library(stringr)
library(splitstackshape)

xlsx <- "F:/Data/PD 2021 Week 19 Input.xlsx"
final <- read_excel(xlsx,'Project Schedule Updates') %>%
  mutate('Week' = paste('Week',`Week`),
         'Commentary' = str_replace_all(`Commentary`,'(\\s+)(?=\\[)','@')) %>%
  cSplit(., 'Commentary', '@') %>%
  pivot_longer(cols=-'Week', names_to='toDrop', values_to = 'Commentary', values_drop_na=TRUE) %>%
  mutate('Project Code' = str_extract(`Commentary`,'(?<=\\[)(\\w+)'),
         'Sub-Project Code' = str_to_lower(str_extract(`Commentary`,'(?<=/)(Mar|Op)')),
         'Task Code' = str_to_title(str_extract(`Commentary`,'(\\w+)(?=\\])')),
         'Abbreviation' = str_to_title(str_extract(`Commentary`,'(\\w+)(?=\\.$)')),
         'Days Noted' = as.integer(str_extract(`Commentary`,'(\\d+)(?=\\sday)')),
         'Detail' = str_extract(`Commentary`,'(?<=\\]\\s)(.*)')) %>%
  merge(., read_excel(xlsx,'Project Lookup Table'), on='Project Code') %>%
  merge(., read_excel(xlsx,'Sub-Project Lookup Table'), on='Sub-Project Code') %>%
  merge(., read_excel(xlsx,'Task Lookup Table'), on='Task Code') %>%
  merge(., read_excel(xlsx,'Owner Lookup Table'), on='Abbreviation') %>%
  select(c('Week', 'Project', 'Sub-Project', 'Task', 'Name', 'Days Noted', 'Detail'))

View(final)
