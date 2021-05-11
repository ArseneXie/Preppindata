library(readxl)
library(dplyr)
library(lubridate)

Sys.setlocale("LC_ALL","English")

final <- read_excel("F:/Data/PD 2021 Wk 18 Input.xlsx") %>%
  rename('Days Difference to Schedule' = 'Completed In Days from Scheduled Date') %>%
  group_by(`Project`,`Sub-project`) %>%
  mutate('Completed Date' = as.Date(`Scheduled Date` %m+% days(`Days Difference to Schedule`)),
         'Completed Weekday' = strftime(`Completed Date`,'%A'),
         'Scope to Build Time' = time_length(max(if_else(`Task`=='Build',`Completed Date`, as.Date('1990-01-01')))-
                                               max(if_else(`Task`=='Scope',`Completed Date`, as.Date('1990-01-01'))),'day'),
         'Build to Delivery Time' = time_length(max(if_else(`Task`=='Deliver',`Completed Date`, as.Date('1990-01-01')))-
                                               max(if_else(`Task`=='Build',`Completed Date`, as.Date('1990-01-01'))),'day')) %>%
  select(c('Project', 'Sub-project', 'Owner', 'Scheduled Date', 'Completed Date', 'Completed Weekday',
           'Task', 'Scope to Build Time', 'Build to Delivery Time', 'Days Difference to Schedule'))
  
View(final)
