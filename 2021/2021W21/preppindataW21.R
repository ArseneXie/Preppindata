library(readxl)
library(dplyr)
library(purrr)
library(stringr)

input <- "F:/Data/PD 2021 Wk 21 Input.xlsx"
sales <-  input %>%
  excel_sheets() %>% 
  set_names() %>%
  map_df(
    ~ read_excel(path = input, sheet = .x,),
    .id = 'Month') %>%
  mutate('Month' = as.integer(str_extract(`Month`,'(\\d+)')),
         'Date' = as.Date(paste('2021',`Month`,`Day of Month`,sep="-")),
         'New Trolley Inventory' = (`Month`>=6),
         'Destination' = trimws(`Destination`),
         'Product' = trimws(str_extract(`Product`,'^([^-]+)')),
         'Price' = as.numeric(str_extract(`Price`,'([\\d\\.]+)'))) %>%
  group_by(`Product`) %>%
  mutate('Average Price per Product' = mean(`Price`),
         'Variance' = `Price` - `Average Price per Product`) %>%
  ungroup() %>%
  group_by(`Destination`,`New Trolley Inventory`) %>%
  mutate('Variance Rank by Destination' = rank(desc(`Variance`))) %>%
  filter(`Variance Rank by Destination` <= 5) %>%
  select(c('New Trolley Inventory','Variance Rank by Destination','Variance','Average Price per Product',
           'Date','Product','first_name', 'last_name', 'email','Price', 'Destination')) %>%
  arrange(`Destination`,`New Trolley Inventory`, `Variance Rank by Destination`)
  
View(sales)