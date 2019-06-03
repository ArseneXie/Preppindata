library(readxl)
library(dplyr)
library(lubridate)

input <- "E:/week5input.xlsx"
sheets <- excel_sheets(input)

final <- read_excel(input,sheet = sheets[1]) %>%
  mutate('Start Date'= parse_date_time( sheets[1],'dby')) %>%
  rbind(., read_excel(input,sheet = sheets[2]) %>% 
          mutate('Start Date'= parse_date_time( sheets[2],'dby'))) %>%
  mutate('True Date' = `Start Date` %m+% days(case_when(`Date`== 'Monday' ~ 0,
                                                `Date`== 'Tuesday' ~ 1,
                                                `Date`== 'Wednesday' ~ 2,
                                                `Date`== 'Thursday' ~ 3,
                                                `Date`== 'Friday' ~ 4,
                                                `Date`== 'Saturday' ~ 5,
                                                TRUE ~ 6)),
         'Statement?' = if_else(grepl('statement',tolower(`Notes`)), 1, 0),
         'Balance?' = if_else(grepl('balance',tolower(`Notes`)), 1, 0),
         'Complaint?' = if_else(grepl('complain',tolower(`Notes`)), 1, 0),
         'Policy Number'= if_else(grepl('#[0-9]+',`Notes`),sub('.*#([0-9]+).*','\\1',`Notes`),NA_character_)) %>%
  na.omit() %>%
  select(-c('Date','Start Date','Notes'))


View(final)