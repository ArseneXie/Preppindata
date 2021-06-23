library(readxl)
library(dplyr)
library(tidyr)
library(fuzzyjoin)

xlsx <- "F:/Data/Answer Smash Input.xlsx"

final <- read_excel(xlsx, sheet = 'Answer Smash') %>%
  regex_inner_join(read_excel(xlsx, sheet = 'Names'),  by = c(`Answer Smash`='Name')) %>%
  regex_inner_join(read_excel(xlsx, sheet = 'Category') %>% 
                     separate(`Category: Answer`, c('Category','Answer'),sep=':\\s'),
                   by = c(`Answer Smash`='Answer'), ignore_case = TRUE) %>%
  merge(read_excel(xlsx, sheet = 'Questions'), by='Q No') %>%
  select(c('Q No', 'Name', 'Question', 'Answer', 'Answer Smash'))

View(final)
