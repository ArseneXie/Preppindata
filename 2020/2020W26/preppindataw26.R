library(dplyr)
library(readxl)

xlsx <- "F:/Data/Matching.xlsx"
sint <- read_excel(xlsx, sheet = 'Internal Data')   
s3rd <- read_excel(xlsx, sheet = '3rd Party Data')   

match <- sint %>%
  merge(., s3rd %>% mutate('ID'=`3rd Party ID`), by=c('ID','Scent')) %>%
  mutate('Status' = 'Matched') 

match_scent <- sint %>% anti_join(., match, by='ID') %>%
  merge(., s3rd %>% anti_join(., match, by='3rd Party ID'), by='Scent') %>%
  mutate('Diff' = abs(`Sales` - `3rd Party Sales`)) %>%
  group_by(`3rd Party ID`) %>%
  filter(`Diff` == min(`Diff`)) %>%
  group_by(`ID`) %>%
  filter(`Diff` == min(`Diff`)) %>%
  select(-'Diff') %>%
  mutate('Status' = 'Matched on Scent')

unmatch_int <- sint %>% 
  anti_join(., match, by='ID') %>%
  anti_join(., match_scent, by='ID') %>%
  mutate('Status' = 'Unmatched - Internal')

unmatch_3rd <- s3rd %>% 
  anti_join(., match, by='3rd Party ID') %>%
  anti_join(., match_scent, by='3rd Party ID') %>%
  mutate('Status' = 'Unmatched - 3rd Party')

final <- bind_rows(match, match_scent, unmatch_int, unmatch_3rd) %>%
  select(c('Status','ID', '3rd Party ID', 'Scent', 'Sales', '3rd Party Sales'))
View(final)