library(readxl)
library(dplyr)
library(tidyr)

input <- "C:/Data/PreppinData/2021W43 Input.xlsx"

final <- read_excel(input,'Business Unit A ') %>%
  mutate('Date lodged' = paste(`Date`,`Month`,`Year`, sep='/')) %>%
  merge(., read_excel(input,'Risk Level'), by.x='Rating', by.y='Risk level') %>%
  select(c('Risk rating', 'Date lodged', 'Status')) %>%
  rename('Rating' = 'Risk rating') %>%
  rbind(., read_excel(input,'Business Unit B ', skip = 5) %>%
          select(c('Rating', 'Date lodged', 'Status'))) %>%
  rename('Status by Process' = 'Status') %>%
  mutate('Status by Lodged' = if_else(as.Date(`Date lodged`,'%d/%m/%Y')<as.Date('1/10/2021','%d/%m/%Y'), 'Opening cases','New cases')) %>%
  pivot_longer(cols=starts_with('Status'), names_to='Type', values_to = 'Status') %>%
  pivot_wider(id_cols='Rating', names_from='Status', values_from='Date lodged', values_fn = length) %>%
  rename('Continuing' = 'In Progress') %>%
  pivot_longer(cols=-'Rating', names_to='Status', values_to = 'Cases') %>%
  mutate_at(vars('Cases'), ~replace_na(., 0)) %>%
  arrange(`Rating`, `Status`)

View(final)
