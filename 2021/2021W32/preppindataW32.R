library(readr)
library(dplyr)
library(tidyr)
library(lubridate)

final <- read_csv("F:/Data/PD 2021 Wk 32 Input - Data.csv",
                  col_types = cols(Date = col_date(format = "%d/%m/%Y"), 
                                   `Date of Flight` = col_date(format = "%d/%m/%Y"))) %>%
  mutate('Flight' = paste(`Departure`,`Destination`, sep=' to '),
         'Days Category' = if_else(time_length(`Date of Flight`-`Date`, 'day')<7,
                                   'less than 7 days until the flight', '7 days of more until the flight'),
         'Sales' = `Ticket Sales`,
         'Avg. daily sales' = `Ticket Sales`) %>%
  select(c('Flight', 'Class', 'Sales', 'Avg. daily sales','Days Category')) %>%
  pivot_wider(id_cols=c('Flight', 'Class'), names_from='Days Category', names_sep = ' ',
              values_from=c('Sales','Avg. daily sales'),
              values_fn = list('Avg. daily sales' = mean, 'Sales' = sum)) %>%
  mutate(across(where(is.numeric), round, 0)) %>%
  select(c('Flight','Class',
           'Avg. daily sales 7 days of more until the flight',
           'Avg. daily sales less than 7 days until the flight',
           'Sales less than 7 days until the flight',
           'Sales 7 days of more until the flight'))

View(final)
