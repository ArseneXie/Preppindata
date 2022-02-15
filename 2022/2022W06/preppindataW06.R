library(dplyr)
library(tidyr)
library(readr)

score <- read_csv("C:/Data/PreppinData/PD 2022 Wk 5 Input.csv") %>%
  pivot_longer(col=-'Student ID', names_to='Subject', values_to = 'Score') %>%
  arrange(`Subject`, -`Score`, `Student ID`) %>%
  group_by(`Subject`) %>% 
  mutate('dummy' = row_number(),
         'NTile' = as.integer(ntile(`dummy`, 6))) %>%
  rowwise() %>%
  mutate('Grade' = intToUtf8(`NTile`+64),
         'Points' = max((6-`NTile`)*2,1)) %>%
  group_by(`Student ID`) %>%
  mutate('Total points per Student' = sum(`Points`),
         'Student Total Score' = sum(`Score`),
         'At least one A' = max(if_else(`Grade`=='A',1,0))) %>%
  group_by(`Grade`) %>%
  mutate('Avg student total points per grade' = round(mean(`Total points per Student`),2)) %>%
  ungroup() %>%
  mutate('Avg Total Score with one A' = mean(if_else(`At least one A`==1, `Student Total Score`, NA_real_), na.rm = TRUE)) %>%
  filter(`Student Total Score`>=`Avg Total Score with one A`) %>%
  filter(`Grade` != 'A')
  
final <- score %>%
  select(c('Student ID', 'Score', 'Subject', 'Points', 'Grade', 'Total points per Student', 'Avg student total points per grade'))
  
quest <- score %>%   
  group_by(`Student ID`) %>%
  mutate('Student Total Score' = sum(`Score`)) %>%
  filter(`Student Total Score`>=`Avg Total Score with one A`) %>%
  select('Student ID') %>%
  n_distinct()
  
View(final)
quest