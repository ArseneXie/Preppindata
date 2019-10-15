library(readxl)
library(dplyr)
library(stringr)
library(lubridate)

Sys.setlocale("LC_ALL","English")

final <- read_excel(path = "E:/PD - Week 34.xlsx", 
                    sheet = "Delivery Schedule") %>%
  mutate('nth' = as.integer(str_extract(`Delivery Schedule`,'^(\\d+)')),
         'Weekday' = str_extract(`Delivery Schedule`,'(?<=\\s).*(?=\\sof)')) %>%
  merge(., read_excel(path = "E:/PD - Week 34.xlsx", 
                      sheet = "Date Scaffold") %>%
          mutate('Month Name' = strftime(`Date`,'%B'),
                 'YearMonth' = strftime(`Date`,'%Y%m'),
                 'Weekday' = strftime(`Date`,'%A'),
                 'one' = 1) %>%
          group_by(`YearMonth`,`Weekday`) %>%
          arrange(`Date`) %>%
          mutate('nth' = cumsum(`one`)),
        on = c('Weekday','nth')) %>%
  arrange(`Date`) %>%
  select(c('Month Name','Weekday','Date','Product','Scent','Supplier','Quantity'))

View(final)  