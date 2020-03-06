library(dplyr)
library(tidyr)
library(readr)
library(stringr)

final <- read_csv("E:/PD 2020 Wk 9 Input - Sheet1.csv", 
                  col_types = cols(Poll = col_character(),
                                   Date = col_character(),
                                   Sample = col_character(),
                                   .default = col_double())) %>%
  drop_na() %>%
  filter(!grepl('Average',`Poll`)) %>%
  mutate('Sample Type' = if_else(grepl('RV',`Sample`),'Registered Voter',
                                 if_else(grepl('LV',`Sample`),'Likely Voter','Unknown')),
         'End Date Year' = if_else(as.integer(str_extract(`Date`,'(\\d+)(?=/\\d+$)'))>10,'2019','2020'),
         'End Date' = as.Date(paste(`End Date Year`,str_extract(`Date`,'(\\d+/\\d+$)')),format='%Y %m/%d')) %>%
  select(-c('Date','Sample','End Date Year')) %>%
  pivot_longer(cols = -c('Poll','Sample Type','End Date'), names_to = 'Candidate', values_to = 'Poll Results') %>%
  group_by(`Poll`,`Sample Type`,`End Date`) %>%
  mutate('Rank' = rank(desc(`Poll Results`),ties.method='max'),
         'Spread from 1st to 2nd Place' = max(`Poll Results`)-nth(`Poll Results`,2,order_by = desc(`Poll Results`))) %>%
  arrange(`End Date`,`Poll`,`Sample Type`,`Rank`)

View(final)
