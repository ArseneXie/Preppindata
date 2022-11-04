library(readxl)
library(dplyr)
library(tidyr)
library(splitstackshape)

xlsx <- "C:/Data/PreppinData/Critical_Role_Campaign_1_Datapack.xlsx"

final <-  read_excel(xlsx, 'dialogue') %>%
  distinct() %>%
  merge(read_excel(xlsx, 'episode_details') %>% 
          select(c('Episode', 'runtime_in_secs')), by='Episode') %>%
  arrange(`Episode`, `time_in_secs`) %>%
  group_by(`Episode`) %>%
  mutate('Duration' = if_else(is.na(lead(`time_in_secs`)), `runtime_in_secs`, lead(`time_in_secs`)) - `time_in_secs`) %>%
  rename('start_time' = 'time_in_secs') %>%
  filter(`section`=='Gameplay') %>%
  cSplit(., 'name', ',') %>%
  pivot_longer(cols=starts_with('name'), names_to='ToDrop', values_to = 'name', values_drop_na=TRUE) %>%
  select(c('Episode', 'name', 'start_time', 'Duration', 'youtube_timestamp', 'dialogue', 'section')) %>%
  distinct()

View(final)
