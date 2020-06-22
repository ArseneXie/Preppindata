library(dplyr)
library(readxl)
library(tidyr)

xlsx <- "F:/Data/Quiz Results.xlsx"

check_answer <- function(myans,correct) { 
  mapply(function(r,c) sum(r==c), strsplit(myans,','), strsplit(correct,',')) }

ans <- read_excel(xlsx, sheet = "Participant Answers") 
correct <- read_excel(xlsx, sheet = "Correct Answers") 

final <- ans %>%
  pivot_longer(., cols=matches('^(Round)'), names_to='Round', values_to='Result') %>%
  merge(correct, by='Round') %>%
  mutate('Score' = check_answer(`Result`,`Answers`)) %>%
  pivot_wider(., id_cols='Name', names_from='Round', values_from='Score') %>%
  mutate('Total Score' = `Round1`+`Round2`+`Round3`+`Round4`+`Round5`,
         'Position' = dense_rank(desc(as.numeric(`Total Score`)))) %>%
  select(c('Position','Name', 'Round1', 'Round2', 'Round3', 'Round4', 'Round5', 'Total Score'))

View(final)
