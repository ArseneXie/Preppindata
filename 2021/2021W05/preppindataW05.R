library(dplyr)
library(readr)

final <- read_csv("F:/Data/Joined Dataset.csv", 
                  col_types = cols(`From Date` = col_date(format = "%d/%m/%Y"))) %>%
  group_by(`Client ID`) %>%
  filter(`From Date` == max(`From Date`)) %>%
  ungroup()

View(final)
