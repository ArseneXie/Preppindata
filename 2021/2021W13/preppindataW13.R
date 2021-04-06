library(readr)
library(dplyr)
library(tidyr)
library(purrr)

df <- dir("F:/Data/2021W13", pattern = "*.csv") %>%
  map(~ read_csv(file.path("F:/Data/2021W13", .))) %>%
  reduce(rbind) %>%
  filter(`Position`!='Goalkeeper' & `Appearances`>0) %>%
  mutate_at(vars('Penalties scored','Freekicks scored'), ~replace_na(., 0)) %>%
  rename('Total Goals' = 'Goals') %>%
  mutate('Open Play Goals' = `Total Goals` - `Penalties scored` - `Freekicks scored`) %>%
  group_by(`Name`, `Position`) %>%
  summarise('Appearances' = sum(`Appearances`),
            'Open Play Goals' = sum(`Open Play Goals`),
            'Total Goals' = sum(`Total Goals`),
            'Headed goals' = sum(`Headed goals`),
            'Goals with right foot' = sum(`Goals with right foot`),
            'Goals with left foot' = sum(`Goals with left foot`),
            'Open Play Goals / Game' = `Open Play Goals`/`Appearances`, 
            .groups = 'drop')

finalA <- df %>%
  mutate('Rank' = rank(desc(`Open Play Goals`), ties.method='min')) %>%
  filter(`Rank`<=20) %>%
  select(c('Rank', 'Name', 'Position', 'Open Play Goals', 'Appearances', 'Open Play Goals / Game', 
           'Headed goals', 'Goals with right foot', 'Goals with left foot', 'Total Goals'))

finalB <- df %>%
  group_by(`Position`) %>%
  mutate('Rank' = rank(desc(`Open Play Goals`), ties.method='min')) %>%
  filter(`Rank`<=20) %>%
  select(c('Rank', 'Name', 'Position', 'Open Play Goals', 'Appearances', 'Open Play Goals / Game', 
           'Headed goals', 'Goals with right foot', 'Goals with left foot', 'Total Goals'))

View(finalA)
View(finalB)
