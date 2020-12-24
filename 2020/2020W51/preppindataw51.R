library(readxl)
library(dplyr)
library(tidyr)
library(stringr)

xlsx <- "F:/Data/NBA Travel Distances.xlsx"

dist <- read_excel(xlsx, sheet = "Travel Distances") %>%
  rename('From City' = !!names(.[1])) %>%
  pivot_longer(., col=-'From City', names_to='To City', values_to='Travel Time') %>%
  filter(`Travel Time` != 0) %>%
  mutate('Hours' = as.integer(str_extract(`Travel Time`,'(\\d+)(?=h)')),
         'Mins' = as.integer(str_extract(`Travel Time`,'(\\d+)(?=m)')),
         'Travel Time in Mins' = ifelse(is.na(`Hours`),0,`Hours`)*60+ifelse(is.na(`Mins`),0,`Mins`))

league <- read_excel(xlsx, sheet = "League Structure") %>%
  mutate('City' = str_extract(`Team`, '(.*)(?=\\s\\w+\\s*$)'))

final <- merge(league, dist, by.x='City', by.y='From City') %>%
  rename('Home City' = 'City',
         'Home Team' = 'Team',
         'Home Conference' = 'Conference',
         'Home Division' = 'Division') %>%
  merge(league %>% select(c('City','Conference')),.,by.x='City', by.y='To City') %>%
  group_by(`Home Team`,`Home Conference`,`Home Division`) %>%
  summarise('Travel Mins' = sum(ifelse(`Home Conference`==`Conference`,1.5,1)*`Travel Time in Mins`), .groups='drop')

View(final)
