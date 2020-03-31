library(dplyr)
library(readxl)
library(stringr)
library(purrr)
library(bizdays)
library(lubridate)

Sys.setlocale("LC_ALL","English")

xlsx <- "E:/Ticket Data.xlsx"
cal <-  create.calendar(name = "mycal", weekdays=c("saturday", "sunday"))

ticket <-  xlsx %>%
  excel_sheets() %>% .[grepl('^...$',.)] %>%
  set_names() %>%
  map_df(
    ~ read_excel(path = xlsx, sheet = .x,)) %>%
  mutate('Department' = trimws(str_extract(`Ticket`,'(?<=/)(.*)(?=/)'))) %>%
  group_by(`Ticket`) %>%
  mutate('MaxTimestamp' = max(`Timestamp`),
         'Current Status' = max(if_else(`Timestamp`==`MaxTimestamp`,`Status Name`,''))) %>% 
  merge(.,read_excel(xlsx, sheet = "SLA Agreements"), by='Department') %>%
  ungroup()

output1 <- ticket %>%
  filter(`Timestamp`==`MaxTimestamp`) %>%
  group_by(`Current Status`) %>%
  summarise('Ticket Count' = n())

output2 <- ticket %>%
  filter(`Status Name`=='Logged') %>%
  mutate('Start Tune' = if_else(weekdays(`Timestamp`)=='Sunday',`Timestamp`+days(1),
                                if_else(weekdays(`Timestamp`)=='Saturday',`Timestamp`+days(2),`Timestamp`)),
         'SLA Due' = bizdays::offset(`Start Tune`,`SLA Agreement`,cal),
         'SLA compare' = if_else(as.Date(`MaxTimestamp`)>`SLA Due`, 'over SLA','under SLA'),
         'Metric' = paste(if_else(`Current Status`=='Closed','Closed','Open'),`SLA compare`)) %>% 
  filter(`Metric`=='Closed over SLA' |  `Metric`=='Open under SLA') %>%
  group_by(`Metric`) %>%
  summarise('Ticket Count' = n())

output3 <- ticket %>%
  filter(`Status Name`=='Logged' & `Current Status`=='Closed') %>%
  mutate('Start Tune' = if_else(weekdays(`Timestamp`)=='Sunday',`Timestamp`+days(1),
                                if_else(weekdays(`Timestamp`)=='Saturday',`Timestamp`+days(2),`Timestamp`)),
         'SLA Due' = bizdays::offset(`Start Tune`,`SLA Agreement`,cal),
         'SLA compare' = if_else(as.Date(`MaxTimestamp`)>`SLA Due`, 0,1)) %>%
  group_by(`Department`) %>%
  summarise('Archieved %' = sum(`SLA compare`)/n()) %>%
  mutate('Rank' =  dense_rank(desc(`Archieved %`))) %>%
  select(c('Rank','Archieved %','Department')) %>%
  arrange(`Rank`)

View(output1)
View(output2)
View(output3)
  