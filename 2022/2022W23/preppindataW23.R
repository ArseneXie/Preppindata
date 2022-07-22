library(readxl)
library(dplyr)
library(tidyr)

xlsx <- "C:/Data/PreppinData/Menu Input.xlsx"

final <-  read_excel(xlsx, 'Orders') %>%
  rename( 'Carl Select' = !!names(.[which(colnames(.)=='Carl')+1]),
          'Tom Select' = !!names(.[which(colnames(.)=='Tom')+1]),
          'Jenny Select' = !!names(.[which(colnames(.)=='Jenny')+1]),
          'Jonathan Select' = !!names(.[which(colnames(.)=='Jonathan')+1])) %>%
  mutate('ID' = row_number(), 
         'Course' = if_else(`Carl` %in% c('Starters', 'Mains', 'Dessert'), `Carl`, NA_character_)) %>%
  fill(`Course`, .direction = 'down') %>%
  pivot_longer(cols=-c('Course', 'ID'), names_to='Guest', values_to='Dish') %>%
  drop_na() %>%
  mutate('Guest'=gsub('\\sSelect','', `Guest`)) %>%
  group_by(`ID`, `Guest`) %>%
  mutate('Select' = n()) %>%
  filter(`Select`==2 & grepl('^\\w',`Dish`)) %>%
  merge(read_excel(xlsx, 'Lookup Table'), by='Dish') %>%
  select(c('Course', 'Guest', 'Recipe ID', 'Dish')) %>%
  arrange(`Guest`, desc(`Course`))
  
View(final)
