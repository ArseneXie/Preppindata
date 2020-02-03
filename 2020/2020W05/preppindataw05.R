library(dplyr)
library(tidyr)
library(readr)

final <- read_csv("E:/PD 2020 Wk 5 Input.csv",
                  col_types = cols(HTf = col_double())) %>%
  drop_na(`HTf`) %>%
  mutate('Rank' = rank(desc(`Diff`), ties.method='min')) %>%
  group_by(`Venue`) %>% 
  summarise('Number of Games' = n(),
            'Best Rank (Standard Competition)' = min(`Rank`),
            'Worst Rank (Standard Competition)' = max(`Rank`),
            'Avg Rank (Standard Competition)' = mean(`Rank`)) %>%
  ungroup() 

View(final)