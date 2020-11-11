library(dplyr)
library(tidyr)
library(readxl)
library(purrr)
library(stringr)

xlsx <- "F:/Data/Prep Air Ticket Sales.xlsx"
country <- read_excel(xlsx, sheet = "Airports")
country_map <- country[['Country']] %>% `names<-`(country[['Airport Code']])

proj <- read_excel(xlsx, sheet = "2020 Projections") %>%
  pivot_longer(.,cols=-'Country', names_to='ToDrop', values_to='proj') %>%
  ungroup() %>%
  group_by(`Country`) %>%
  summarise('Factor' = (400+sum(if_else(str_sub(`proj`,1,1)=='M',-1,1)*as.integer(str_remove_all(`proj`,'\\D'))))/100)
proj_map <- proj[['Factor']] %>% `names<-`(proj[['Country']])

final <- xlsx %>%
  excel_sheets() %>% .[grepl('.*Sales.*',.)] %>%
  set_names() %>%
  map_df(
    ~ read_excel(path = xlsx, sheet = .x,),
    .id = 'Type') %>%
  mutate('Type' = if_else(grepl('.*Target.*',`Type`),'Target Value','Value')) %>%
  select(-c('Date')) %>%
  pivot_wider(., names_from='Type', values_from='Value', values_fn = sum) %>%
  rowwise() %>%
  mutate('Origin Country' = country_map[[`Origin`]],
         'Destination Country' = country_map[[`Destination`]],
         'Factor' = proj_map[[`Destination Country`]],
         'Value' = `Value`*`Factor`,
         'Target Value' = `Target Value`*`Factor`,
         'Variance to Target' = `Value` - `Target Value`) %>%
  select(c('Origin', 'Origin Country', 'Destination', 'Destination Country', 'Value', 'Target Value', 'Variance to Target'))

View(final)
