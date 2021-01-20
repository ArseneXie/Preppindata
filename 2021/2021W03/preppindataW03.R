library(readxl)
library(dplyr)
library(tidyr)
library(purrr)
library(lubridate)

input <- "F:/Data/PD 2021 Wk 3 Input.xlsx"
df <-  input %>%
  excel_sheets() %>% 
  set_names() %>%
  map_df(
    ~ read_excel(path = input, sheet = .x,),
    .id = 'Store') %>%
  pivot_longer(cols=-c('Date','Store'), 
               names_to=c('Customer Types','Product'), names_pattern='(\\w+)\\W+(\\w+)',
               values_to = 'Products Sold') %>%
  mutate('Quarter' = quarter(`Date`))

finalA <- df %>%
  group_by(`Product`,`Quarter`) %>%
  summarise('Products Sold' = sum(`Products Sold`))

finalB <- df %>%
  group_by(`Store`,`Customer Types`,`Product`) %>%
  summarise('Products Sold' = sum(`Products Sold`))

View(finalA)
View(finalB)
