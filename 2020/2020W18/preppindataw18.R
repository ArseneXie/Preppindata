library(dplyr)
library(readxl)
library(tidyr)
library(stringr)
library(purrr)

xlsx <- 'E:/Liverpool Lineups.xlsx'

data_head <- read_excel(xlsx, col_names = FALSE, skip = 4, n_max = 4) %>%
  
  mutate('col_level' = row_number()) %>%
  filter(`col_level`<=2) %>%
  gather(., key='var', value='cols', -'col_level') %>%
  group_by(`col_level`) %>% 
  fill(`cols`) %>%
  spread(.,`col_level`, `cols`) %>%
  mutate('col_name' = ifelse(grepl('^sub',`2`),`2`,paste(`1`,`2`))) %>%
  arrange(as.integer(str_extract(`var`,'\\d+'))) %>% 
  group_by(`col_name`) %>% 
  mutate('Indicator' = cumsum(ifelse(`col_name`==lag(`col_name`, default='#'),1,0))) %>%
  mutate('fin_col_name' = ifelse(`Indicator`==0,`col_name`,paste0(`col_name`,'.',`Indicator`)))

data <- read_excel(xlsx, skip = 7 ,col_names = FALSE) %>%
  rename_all(funs(data_head[['fin_col_name']][as.integer(str_extract(.,'\\d+'))])) %>%
  map(~.x) %>%
  discard(~all(is.na(.x))) %>%
  map_df(~.x) 



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