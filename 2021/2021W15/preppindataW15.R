library(readr)
library(dplyr)
library(tidyr)
library(readxl)
library(splitstackshape)

Sys.setlocale("LC_ALL","English")
xlsx <- "F:/Data/Menu and Orders.xlsx"

df <- read_excel(xlsx, sheet = 'MENU') %>% 
  pivot_longer(cols=c('Pizza','Pasta', 'House Plates'), names_to='Type', values_to = 'Name', values_drop_na = TRUE) %>%
  mutate('ID' = as.character(if_else(`Type`=='Pizza', `Pizza ID`, if_else(`Type`=='Pasta', `Pasta ID`, `House Plates ID`))),
         'Price' = if_else(`Type`=='Pizza', `Pizza Price`, if_else(`Type`=='Pasta', `Pasta Price`, `House Plates Prices`))) %>%
  select('ID', 'Price') %>%
  merge(.,read_excel(xlsx, sheet = 'Order') %>% cSplit(., 'Order', '-', type.convert = FALSE) %>%
          pivot_longer(cols=starts_with('Order_'), names_to = c(".value",NA), names_pattern = '(Order)_(.*)', values_drop_na = TRUE),
        by.x='ID', by.y='Order') %>%
  mutate('Weekday' = strftime(`Order Date`,'%A'), 
         'Price' = if_else(`Weekday`=='Monday',0.5,1)*`Price`)

finalA <- df %>%
  group_by(`Weekday`) %>%
  summarise('Price' = sum(`Price`), .groups ='drop')

finalB <- df %>%
  group_by(`Customer Name`) %>%
  summarise('Count Items' = n(), .groups ='drop') %>%
  filter(`Count Items` == max(`Count Items`))

View(finalA)
View(finalB)
