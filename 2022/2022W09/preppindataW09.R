library(readxl)
library(dplyr)
library(tidyr)
library(lubridate)
library(stringr)

xlsx <- "C:/Data/PreppinData/Sample - Superstore.xls"

status_transfer <- function(order_str){
  ret <- str_replace_all(order_str, '(^1)', 'N') %>%
    str_replace_all(., '(?<!0)(1)', 'C') %>%
    str_replace_all(., '(?<=0)(1)', 'R') %>%
    str_replace_all(., '0', 'S') %>%
    str_pad(., 4, 'left', '-')
  return(ret)}

customer_class <- function(class_code){
  ret <- case_when(
    class_code == 'N' ~ 'New',
    class_code == 'C' ~ 'Consistent',
    class_code == 'S' ~ 'Sleeping',
    class_code == 'R' ~ 'Returning',
    TRUE ~ '-' )
  return(ret)}

sales <- read_excel(xlsx, 'Orders') %>% mutate('Year' = year(`Order Date`))

customer <- sales %>%
  select(c('Customer ID', 'Customer Name', 'Year')) %>%
  distinct() %>%
  group_by(`Customer ID`) %>%
  mutate('Order?' = 1,
         'First Purchase' = min(`Year`)) %>%
  ungroup() %>%
  pivot_wider(names_from = 'Year', values_from = 'Order?', values_fill = 0) %>%
  pivot_longer(cols=matches('^\\d'), names_to = 'Year', values_to = 'Order?', names_transform = list('Year'=as.integer)) %>%
  group_by(`Customer ID`) %>%
  mutate('Position' = `Year` - min(`Year`) + 1,
         'Power' = max(`Year`) - `Year`, 
         'OrderString' = status_transfer(as.character(sum(`Order?`*10^`Power`))),
         'Customer Classification' = customer_class(substr(`OrderString`, `Position`, `Position`))) %>%
  filter(`Customer Classification` != '-') %>%
  select(c('Customer ID', 'Customer Name', 'First Purchase', 'Year', 'Order?', 'Customer Classification'))
  
cohort <- customer %>%
  group_by(`First Purchase`, `Year`) %>%
  summarise('Order?' = sum(`Order?`), .groups='drop') %>%
  arrange(`First Purchase`, `Year`) %>%
  group_by(`First Purchase`) %>%
  mutate('YoY Difference' = `Order?` - lag(`Order?`)) %>%
  select(c('First Purchase', 'Year', 'YoY Difference'))
  
final <- merge(customer, cohort, by=c('First Purchase', 'Year')) %>%
  merge(., sales, by=c('Customer ID', 'Customer Name', 'Year'), all.x=TRUE)

View(final)