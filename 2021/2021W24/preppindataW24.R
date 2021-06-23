library(readxl)
library(dplyr)
library(lubridate)
library(fuzzyjoin)

final <- read_excel(path = "F:/Data/Absenteeism Scaffold.xlsx", sheet = 'Reasons') %>%
  mutate('End Date' = `Start Date` %m+% days(`Days Off`)-1) %>%
  fuzzy_full_join(., as.data.frame(seq(as.Date("2021/4/1"), as.Date("2021/5/31"),by="day")) %>%
                    `colnames<-`(c('Date')),
                  by=c('Start Date'='Date', 'End Date'='Date'), match_fun=list(`<=`,`>=`)) %>%
  group_by(`Date`) %>%
  summarise('Number of people off each day' = sum(!is.na(`Name`)), .groups='drop')

ans1 <- final %>%
  filter(`Number of people off each day` == max(`Number of people off each day`)) %>%
  .[['Date']]
  
ans2 <- final %>%
  filter(`Number of people off each day` == 0) %>%
  nrow(.)

View(final)
