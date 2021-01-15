library(dplyr)
library(tidyr)
library(readr)
library(stringr)
library(stringi)
library(lubridate)

final <- read_csv("F:/Data/PD 2021 Wk 1 Input - Bike Sales.csv", 
                  col_types = cols(`Date` = col_date(format = "%d/%m/%Y"))) %>%
  separate(`Store - Bike`,c('Store','Bike'),sep='\\s+-\\s+') %>%
  mutate('Bike' = stri_replace_all_regex(`Bike`, pattern = c('^M.*', '^G.*', '^R.*'), 
                                         replacement = c('Mountain', 'Gravel', 'Road'), vectorize_all = FALSE),
         'Quarter' = quarter(`Date`),
         'Day of Month' = day(`Date`)) %>%
  filter(`Order ID`>10) %>%
  select(c('Quarter', 'Day of Month', 'Store', 'Bike', 'Order ID', 'Customer Age', 'Bike Value', 'Existing Customer?'))

View(final)
