library(dplyr)
library(readxl)
library(tidyr)
library(stringr)
library(splitstackshape)

xlsx <- "E:/PD 2020W17 Shows and Devices.xlsx"
show_list <- read_excel(xlsx, sheet = "Netflix Shows") %>%
  distinct() %>%
  mutate('Show' = str_trim (toupper(str_extract(`TV Shows/Movies`,'([^\\(]+)'))))

dev_list <- read_excel(xlsx, sheet = "Devices") %>%
  distinct() %>%
  mutate('Using' = tolower(`Device`))

survey <- read_excel('E:/PD 2020W17 Survey.xlsx', sheet = 1) %>%
  select(-'Timestamp') %>%
  distinct() 

device <- survey %>%
  select('How have you been watching Netflix? (Phone, TV, etc.)') %>%
  rename('Using' = !!names(.[1])) %>%
  cSplit(., 'Using', ',|&') %>%
  pivot_longer(.,cols=matches('^Using'), names_to='ToDrop', values_to='Using', values_drop_na = TRUE) %>%
  mutate('Using' = tolower(`Using`)) %>%
  filter(`Using`!='etc.') %>%
  merge(.,dev_list,by='Using',all.x=TRUE) %>%
  mutate_at(vars('Device'), ~replace_na(., 'Other')) %>%
  group_by(`Device`) %>%
  summarise('Count' = n())

show_in_Q <- colnames(survey)[grepl('.*rate.*\\w\\?', colnames(survey))] %>%
  str_extract(.,'(?<=rate\\s)(.*)(?=\\?)') %>%
  toupper(.)

show <- rbind(survey %>%
  select(c('How would you rate "Other"?','What have you been binging during lockdown?')) %>%
  rename('Rate' = !!names(.[1]), 'lockdown' = !!names(.[2])) %>%
  cSplit(., 'lockdown', ',') %>%
  pivot_longer(.,cols=matches('^lockdown'), names_to='ToDrop', values_to='Show', values_drop_na = TRUE) %>%
  mutate('Show'= toupper(`Show`)) %>%
  filter(is.na(match(`Show`,show_in_Q))) %>%
  merge(.,show_list,by='Show') %>%
  select(c('Show','Rate')),
  survey %>%
  select(matches("lockdown") | matches("rate [^\"]")) %>%
  rename('lockdown' = !!names(.[1])) %>%
  pivot_longer(.,cols=matches('rate'), names_to='Question', values_to='Rate', values_drop_na = TRUE) %>%
  mutate('Show' =  toupper(str_extract(`Question`,'(?<=rate\\s)(.*)(?=\\?)'))) %>%
  filter(str_detect(toupper(`lockdown`),`Show`)) %>%
  select(c('Show','Rate'))) %>%
  group_by(`Show`) %>%
  summarise('Rate' = mean(`Rate`)) %>%
  mutate('Rank' = dense_rank(desc(`Rate`)))

View(device)
View(show)