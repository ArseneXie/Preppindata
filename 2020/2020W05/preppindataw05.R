library(dplyr)
library(tidyr)
library(readxl)
library(stringr)
library(purrr)

Sys.setlocale('LC_ALL','English')
input <- "E:/PD - NBA Results.xlsx"
team_list <- read_excel(input,'Team List') %>% select(c('Team','Conference'))

final <-  input %>% excel_sheets() %>% .[grepl('Results$',.)] %>%
  map_df(~ read_excel(path = input, sheet = .x, range = cell_cols('A:F'))) %>%
  rename('PTS'=!!names(.[4]),'PTS_H'=!!names(.[6])) %>%
  drop_na('PTS') %>%
  merge(., team_list %>% rename('Away Conf'='Conference'), by.x='Visitor/Neutral', by.y='Team') %>%
  merge(., team_list %>% rename('Home Conf'='Conference'), by.x='Home/Neutral', by.y='Team') %>%
  mutate('Date' = as.Date(str_remove(`Date`,'^\\w+\\s'),'%b %d %Y'),
         'In Conf' = if_else(`Away Conf`==`Home Conf`,1,0),
         'Away WL' = if_else(`PTS`>`PTS_H`,'W','L'),
         'Home WL' = if_else(`PTS`>`PTS_H`,'L','W')) %>%
  unite('Away','Away Conf','Visitor/Neutral','Away WL',sep='_') %>%
  unite('Home','Home Conf','Home/Neutral','Home WL',sep='_') %>%
  select(c('Date','In Conf','Away','Home')) %>%
  gather(., key='Away Home',value='Team Game Data','Away','Home') %>%
  separate('Team Game Data',c('Conference','Team','Win Lose'),sep='_') %>%
  group_by(`Team`) %>%
  mutate('Last N' = rank(desc(`Date`))) %>%
  group_by(`Conference`,`Team`,`Win Lose`) %>%
  summarise('All' = n(),
            'Away' = sum(if_else(`Away Home`=='Away',1,0)),
            'Home' = sum(if_else(`Away Home`=='Home',1,0)),
            'Conf' = sum(`In Conf`),
            'L10' = sum(if_else(`Last N`<=10,1,0)), 
            'Strk' = min(`Last N`)) %>%
  gather(., key='WL Type',value='R2CVal','All','Away','Home','Conf','L10','Strk') %>%
  unite('R2CCol','WL Type','Win Lose',sep=' ') %>%
  spread('R2CCol','R2CVal') %>%
  unite('Conf','Conf W','Conf L',sep='-') %>%
  unite('Home','Home W','Home L',sep='-') %>%
  unite('Away','Away W','Away L',sep='-') %>%
  unite('L10','L10 W','L10 L',sep='-') %>%
  rename('W'='All W', 'L'='All L') %>%
  mutate('Pct' = round(`W`/(`W`+`L`),3),
         'Strk' = if_else(`Strk W`==1,paste0('W',`Strk L`-1),paste0('L',`Strk W`-1))) %>%
  group_by(`Conference`) %>%
  mutate('Rank' = rank(desc(`Pct`),ties.method='max')) %>%
  select(c('Conference','Rank','Team','W','L','Pct','Conf','Home','Away','L10','Strk')) %>%
  ungroup()

final_east <- final %>% filter(`Conference`=='Eastern') %>% select(-'Conference') %>% arrange(`Rank`)  
final_west <- final %>% filter(`Conference`=='Western') %>% select(-'Conference') %>% arrange(`Rank`) 
View(final_east)
View(final_west)