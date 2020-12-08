library(dplyr)
library(readxl)
library(zoo)

xlsx <- "F:/Data/2020W47 Input.xlsx"
final <- read_excel(xlsx, sheet = "Delays") %>%
  {. ->> tmp} %>%
  na.locf(., na.rm=FALSE) %>%
  .[!is.na(tmp$Delay),] %>%
  mutate("Airport" = if_else(grepl('JKF',`Airport`), 'JFK', `Airport`)) %>%
  group_by(`Airport`,`Type`) %>%
  summarise('Total Delay' = sum(`Delay`),
            'Delay flights' = n(), .groups = 'drop') %>%
  merge(.,read_excel(xlsx, sheet = "On Time"), by=c('Airport','Type')) %>%
  mutate('Total flights' = `Number of flights`+`Delay flights`,
         'Avg Delay (mins)' = round(`Total Delay`/`Total flights`,2),
         '% Flights Delayed' = round(`Delay flights`/`Total flights`*100,2)) %>%
  select(c('Airport', 'Type', '% Flights Delayed', 'Avg Delay (mins)'))

View(final)
