library(readxl)
library(dplyr)
library(tidyr)
library(purrr)

input <- "F:/Data/NPS Input.xlsx"
final <-  input %>%
  excel_sheets() %>% 
  set_names() %>%
  map_df(~ read_excel(path = input, sheet = .x,)) %>%
  `colnames<-`(c('Airline', 'CustomerID', 'like')) %>%
  group_by(`Airline`) %>%
  filter(n()>=50) %>%
  ungroup() %>%
  mutate('Class' = if_else(`like`<=6,'Detractors',if_else(`like`<=8,'Passive','Promoters'))) %>%
  pivot_wider(id_cols='Airline', names_from='Class', values_from='CustomerID', values_fn=list(`CustomerID` = length)) %>%
  mutate('Promoters%' = as.integer(`Promoters`/(`Promoters`+`Passive`+`Detractors`)*100),
         'Detractors%' = as.integer(`Detractors`/(`Promoters`+`Passive`+`Detractors`)*100),
         'NPS' = `Promoters%` - `Detractors%`,
         'Z-Score' = round((`NPS`-mean(`NPS`))/sd(`NPS`),2)) %>%
  filter(`Airline`=='Prep Air') %>%
  select(c('Airline', 'NPS', 'Z-Score'))

View(final)
