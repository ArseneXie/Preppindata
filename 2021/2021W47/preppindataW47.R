library(readxl)
library(dplyr)
library(tidyr)
library(lubridate)
options("scipen"=100, "digits"=7)

xlsx <- "C:/Data/PreppinData/top_female_poker_players_and_events.xlsx"
final <- read_excel(xlsx, 'top_100') %>%
  select(c('name', 'all_time_money_usd', 'player_id')) %>%
  merge(read_excel(xlsx, 'top_100_poker_events'), by='player_id') %>%
  group_by(`name`) %>%
  summarise('number_of_events' = n(), 
            'event_country' = n_distinct(`event_country`),
            'total_prize_money' = max(`all_time_money_usd`),
            'biggest_win' = max(if_else(is.na(`prize_usd`),0,`prize_usd`)),
            'percent_won' = sum(if_else(`player_place`=='1st',1,0))/`number_of_events`,
            'career_length' = time_length(difftime(max(`event_date`),min(`event_date`)),'years')) %>%
  pivot_longer(cols=-'name', names_to='metric', values_to='raw_value') %>%
  group_by(`metric`) %>%
  mutate('scaled_value' = rank(`raw_value`,  ties.method='average'))

View(final)  
