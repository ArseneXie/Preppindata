library(readxl)
library(dplyr)
library(tidyr)
library(stringr)
library(purrr)

xlsx <- "F:/Data/InternationalPenalties.xlsx"
competition <-  xlsx %>%
  excel_sheets() %>% 
  set_names() %>%
  map_df(~ read_excel(path = xlsx, sheet = .x,) %>% `colnames<-`(str_to_title(names(.))),.id = 'Source') %>%
  mutate('Winner' = str_replace_all(trimws(`Winner`,whitespace='[\\h\\v]'), 'West Germany', 'Germany'),
         'Loser' = str_replace_all(trimws(`Loser`,whitespace='[\\h\\v]'), 'West Germany', 'Germany'),
         'Winner Penalty Scored' = if_else(str_detect(`Winning Team Taker`, '(scored)'),1,0),
         'Loser Penalty Scored' = if_else(str_detect(`Losing Team Taker`, '(scored)'),1,0))

finalA <- competition %>%
  select(c('Source', 'No.', 'Winner', 'Loser')) %>% distinct() %>%
  pivot_longer(cols=c('Winner', 'Loser'), names_to='WL', values_to='Team') %>%
  group_by(`Team`) %>%
  summarise('Shootouts' = sum(if_else(`WL`=='Winner', 1, 0)),
            'Total Shootouts' = n()) %>%
  filter(`Shootouts` > 0) %>%
  mutate('Shootouts Win %' = round(`Shootouts`*100/`Total Shootouts`),
         'Win % Rank' = dense_rank(desc(`Shootouts Win %`))) %>%
  select(c('Win % Rank', 'Shootouts Win %', 'Total Shootouts', 'Shootouts', 'Team')) %>%
  arrange(`Win % Rank`, desc(`Shootouts`))

finalB <- competition %>%
  select(c('Winner', 'Loser', 'Winner Penalty Scored', 'Loser Penalty Scored')) %>%
  pivot_longer(cols=c('Winner', 'Loser'), names_to='WL', values_to='Team') %>%
  mutate('Penalties Scored' = if_else(`WL`=='Winner',`Winner Penalty Scored`, `Loser Penalty Scored`)) %>%
  drop_na(`Penalties Scored`) %>%
  group_by(`Team`) %>%
  summarise('Penalties Scored' = sum(`Penalties Scored`),
            'Total Penalties' = n()) %>%
  mutate('Penalties Missed' = `Total Penalties` - `Penalties Scored`,
         '% Total Penalties Scored' = round(`Penalties Scored`*100/`Total Penalties`),
         'Penalties Scored % Rank' = dense_rank(desc(`% Total Penalties Scored`))) %>%
  select(c('Penalties Scored % Rank', '% Total Penalties Scored', 'Penalties Missed', 'Penalties Scored', 'Team')) %>%
  arrange(`Penalties Scored % Rank`, desc(`Penalties Scored`))

finalC <- competition %>%
  select(c('Penalty Number', 'Winner Penalty Scored', 'Loser Penalty Scored')) %>%
  pivot_longer(cols=-'Penalty Number', names_to='Dummy', values_to='Penalties Scored') %>% drop_na() %>%
  group_by(`Penalty Number`) %>%
  summarise('Penalties Scored' = sum(`Penalties Scored`),
            'Total Penalties' = n()) %>%
  mutate('Penalties Missed' = `Total Penalties` - `Penalties Scored`,
         'Penalties Scored %' = round(`Penalties Scored`*100/`Total Penalties`),
         'Rank' = dense_rank(desc(`Penalties Scored %`))) %>%
  select(c('Rank', 'Penalties Scored %', 'Penalties Missed', 'Penalties Scored', 'Total Penalties', 'Penalty Number')) %>%
  arrange(`Rank`, `Penalty Number`)

View(finalA)
View(finalB)
View(finalC)

