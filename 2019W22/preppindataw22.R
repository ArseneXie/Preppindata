library(dplyr)
library(readr)
library(zoo)        

final <- read_csv("E:/PD Wk 22 Input.csv", 
                  col_types = cols(Date = col_date(format = "%d/%m/%Y"))) %>%
  mutate('Moving Avg Sales'=rollapply(`Sales`,7,mean,align='right',fill=NA)) %>%
  select(-'Sales')

View(final)
