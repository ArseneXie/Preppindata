library(readxl)
library(dplyr)
library(tidyr)

xlsx <- "C:/Data/PreppinData/input_pkmn_stats_and_evolutions.xlsx"
combat_factors <- c('hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed')

stats <- read_excel(xlsx, 'pkmn_stats') %>%
  select(-c('height', 'weight', 'evolves_from')) %>%
  pivot_longer(cols=all_of(combat_factors), names_to = 'combat_factors', values_to = 'value')

final <- read_excel(xlsx, 'pkmn_evolutions') %>% 
  drop_na(`Stage_2`) %>%
  merge(., stats %>% rename('Stage_1'='name'), by='Stage_1') %>% 
  merge(., stats %>% 
          select(c('name', 'combat_factors', 'value')) %>% 
          rename('Stage_2'='name'), by=c('Stage_2', 'combat_factors'), suffixes = c(".s1","")) %>%
  merge(., stats %>% 
          select(c('name', 'combat_factors', 'value')) %>% 
          rename('Stage_3'='name'), by=c('Stage_3', 'combat_factors'), suffixes = c(".s2",".s3"), all.x=TRUE) %>%
  group_by(`Stage_1`, `Stage_2`, `Stage_3`, `pokedex_number`, `gen_introduced`) %>%
  summarise('intial_combat_power' = sum(`value.s1`), 
            'final_combat_power' = if_else(is.na(max(`Stage_3`)), sum(`value.s2`), sum(`value.s3`)), 
            'combat_power_increase' = (`final_combat_power`-`intial_combat_power`)/`intial_combat_power`, .groups = 'drop') %>%
  arrange(`combat_power_increase`)

View(final)
