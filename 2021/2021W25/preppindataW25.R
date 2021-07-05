library(readxl)
library(dplyr)
library(tidyr)
library(stringr)
library(purrr)

xlsx <- "F:/Data/2021W25 Input.xlsx"

grp <- read_excel(xlsx, sheet = 'Evolution Group') %>%
  filter(`Starter?`==0 & `Legendary?`==0) %>%
  select(c('#','Evolution Group')) %>%
  mutate('#' = as.integer(str_remove(`#`,'\\D')))

evo <- read_excel(xlsx, sheet = 'Evolutions') %>% 
  select(c('Evolving from', 'Evolving to'))

gen1 <- read_excel(xlsx, sheet = 'Gen 1') %>%
  select(c('#','Name')) %>%
  drop_na() %>%
  merge(grp, by='#') 

mega <- xlsx %>%
  excel_sheets() %>% .[grepl('(Mega Evolutions|Alolan|Galarian|Gigantamax)',.)] %>%
  set_names() %>%
  map_df( ~ read_excel(xlsx, sheet = .x,)) %>%
  mutate('Name' = str_remove(`Name`, '^(\\w+\\s)')) %>%
  distinct()

final <- rbind(merge(evo, gen1, by.x='Evolving from', by.y='Name') %>%
                 rename('Pokemon' = 'Evolving to') %>%
                 select(c('Evolution Group', 'Pokemon')),
               merge(evo, gen1, by.x='Evolving to', by.y='Name') %>%
                 rename('Pokemon' = 'Evolving from') %>%
                 select(c('Evolution Group', 'Pokemon'))) %>%
  distinct() %>%
  mutate('Check' = as.integer(`Pokemon` %in% mega$Name)) %>%
  group_by(`Evolution Group`) %>%
  mutate('Group Check' = sum(`Check`)) %>%
  filter(`Group Check`==0) %>%
  merge(read_excel(xlsx, sheet = 'Unattainable in Sword & Shield') %>%
          rename('Evolution Group'='Name'), by='Evolution Group') %>%
  merge(read_excel(xlsx, sheet = 'Anime Appearances'), by='Pokemon') %>%
  group_by(`Evolution Group`) %>%
  summarise('Appearances' = n_distinct(`Episode`), .groups='drop') %>%
  mutate('The Worst Pokemon' = as.integer(rank(`Appearances`, ties.method='min'))) %>%
  select(c('The Worst Pokemon', 'Evolution Group', 'Appearances')) %>%
  arrange(`Appearances`) 

View(final)
