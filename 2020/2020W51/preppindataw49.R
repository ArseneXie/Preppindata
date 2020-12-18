library(readxl)
library(dplyr)
library(purrr)

input <- "F:/Data/NBA 2018_19 Results.xlsx"

final <-  input %>%
  excel_sheets() %>% 
  set_names() %>%
  map_df(
    ~ read_excel(path = input, sheet = .x,))  %>%
  select('Date', ends_with('Neutral'), starts_with('PTS')) %>%
  `colnames<-`(c('Date','Visitor','Home','Visitor PTS','Home PTS')) %>%
  pivot_longer(., cols=c('Visitor','Home'), names_to='Type', values_to='Team') %>%
  mutate('Win' = as.integer(if_else(`Type`=='Home',`Home PTS`>`Visitor PTS`,`Visitor PTS`>`Home PTS`))) %>%
  group_by(`Team`) %>%
  mutate('Game Number per Team' = row_number(`Date`),
         'Win' = cumsum(`Win`)) %>%
  group_by(`Game Number per Team`) %>%
  mutate('Rank' = rank(interaction(desc(`Win`),`Team`,lex.order=T))) %>%
  select(c('Rank','Win','Team', 'Game Number per Team'))

View(final)
