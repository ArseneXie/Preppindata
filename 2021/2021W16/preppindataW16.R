library(readr)
library(dplyr)
library(tidyr)
library(stringr)

data <- read_csv("F:/Data/PL Fixtures.csv") %>% drop_na() 
big6 <- c('Arsenal','Chelsea','Liverpool','Man Utd','Man City','Spurs')
  
get_position <- function(df) {
  df <- df %>%
    mutate('Home Score' = as.integer(str_extract(`Result`, '^(\\d+)')),
           'Away Score' = as.integer(str_extract(`Result`, '(\\d+)$')),
           'Home Goal Difference' = `Home Score` - `Away Score`,
           'Away Goal Difference' = -1*`Home Goal Difference`,
           'Home Point' = if_else(`Home Goal Difference`>0, 3, if_else(`Home Goal Difference`==0, 1, 0)),
           'Away Point' = if_else(`Away Goal Difference`>0, 3, if_else(`Away Goal Difference`==0, 1, 0)))
  
  fin <- bind_rows( df %>% select(starts_with('Home')),
                    df %>% select(starts_with('Away'))) %>%
    mutate_if(is.numeric, list(~replace_na(.,0))) %>%
    mutate('Team' = if_else(is.na(`Away Team`),`Home Team`,`Away Team`)) %>%
    group_by(`Team`) %>%
    summarise('Total Games Played' = n(),
              'Total Points' = sum(`Home Point`+`Away Point`),
              'Goal Difference' = sum(`Home Goal Difference`+`Away Goal Difference`), .groups='drop') %>%
    mutate('Position' = as.integer(rank(interaction(desc(`Total Points`), desc(`Goal Difference`), lex.order=T)))) %>%
    select(c('Position', 'Team', 'Total Games Played', 'Total Points', 'Goal Difference')) 
  return(fin)
}  
  
finA <- get_position(data) %>% 
  arrange(`Position`)

finB <- get_position(data %>% 
                       filter(!(`Home Team` %in% big6 | `Away Team` %in% big6))) %>%
  merge(.,finA %>% select(c('Team', 'Position')) %>% rename('Position Original' = `Position`), by='Team') %>%
  mutate('Position change' = `Position Original` - `Position`) %>%
  select(c('Position change', 'Position', 'Team', 'Total Games Played', 'Total Points', 'Goal Difference')) %>% 
  arrange(`Position`)

View(finA)
View(finB)
