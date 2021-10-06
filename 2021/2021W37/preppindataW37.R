library(readxl)
library(dplyr)
library(lubridate)

contract <- read_excel("F:/Data/2021 Week 37 Input.xlsx", sheet = "Contract Details")
                
final <- contract[rep(seq_len(nrow(contract)), contract[['Contract Length (months)']]),] %>%
  group_by(`Name`) %>%
  mutate('rownum' = row_number(`Name`),
         'Payment Date' = `Start Date` %m+% months(`rownum`-1),
         'Cumulative Monthly Cost' = `Monthly Cost`*`rownum`) %>%
  select(c('Name', 'Payment Date', 'Monthly Cost', 'Cumulative Monthly Cost'))

View(final)
