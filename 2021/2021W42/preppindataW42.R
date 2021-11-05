library(readr)
library(dplyr)
library(tidyr)

Sys.setlocale("LC_ALL","English")

final <- read_csv("C:/Data/PreppinData/Prep Generate Rows datasets - Charity Fundraiser.csv",
                  col_types =cols(`Date` = col_date(format = "%d/%m/%Y"))) %>%
  complete(., `Date` = full_seq(`Date`, period = 1)) %>%
  arrange(`Date`) %>%
  fill(`Total Raised to date`) %>%
  mutate('Days into fund raising' = row_number()-1,
         'Value raised per day' = if_else(`Days into fund raising`>0, `Total Raised to date`/`Days into fund raising`, NA_real_), 
         'Date' = weekdays(`Date`)) %>%
  group_by(`Date`) %>%
  mutate('Average raised per weekday' = mean(`Value raised per day`, na.rm=TRUE))

View(final)
