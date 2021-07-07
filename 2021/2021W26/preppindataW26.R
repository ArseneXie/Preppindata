library(readr)
library(dplyr)
library(tidyr)
library(zoo)

rev <- read_csv("F:/Data/PD 2021 Wk 26 Input - Sheet1.csv",
                col_types = cols(Date = col_date(format = "%d/%m/%Y")))

final <- rbind(rev, rev %>% 
                 group_by(`Date`) %>% 
                 summarise('Revenue' = sum(`Revenue`), .groups = 'drop',
                           'Destination' = 'All')) %>%
  group_by(`Destination`) %>%
  arrange(`Date`, .by_group = TRUE) %>%
  mutate('Rolling Week Avg' = rollapply(`Revenue`,7,mean,align='center', partial = TRUE, fill=NA),
         'Rolling Week Total' = rollapply(`Revenue`,7,sum,align='center', partial = TRUE, fill=NA))

View(final)
