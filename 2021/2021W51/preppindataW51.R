library(readr)
library(dplyr)
library(tidyr)

df <- read_csv("C:/Data/PreppinData/2021W51 Input.csv",
               col_types =cols(`Order Date` = col_date(format = "%d/%m/%Y"))) %>%
  separate(`OrderID`, c('Store','OrderID'),sep='-') %>%
  mutate('Returned' = as.integer(!is.na(`Return State`)),
         'Unit Price' = as.numeric(substring(`Unit Price`, 2)),
         'Sales' = `Unit Price`*`Quantity`) %>%
  group_by(`Store`) %>%
  mutate('Store First Order' = min(`Order Date`)) %>%
  group_by(`Customer`) %>%
  mutate('Customer First Order' = min(`Order Date`),
         'Number of Orders' = n_distinct(`OrderID`),
         'Return %' = round(sum(`Returned`)/n(),2)) %>%
  group_by(`Product Name`) %>%
  mutate('Product First Sold' = min(`Order Date`)) %>%
  ungroup() %>%
  mutate('StoreID' = dense_rank(interaction(`Store First Order`, `Store`, lex.order=T)),
         'CustomerID' = dense_rank(interaction(`Customer First Order`, `Customer`, lex.order=T)),
         'ProductID' = dense_rank(interaction(`Product First Sold`, tolower(`Product Name`), lex.order=T)))
  
fact <- df %>%
  select(c('StoreID', 'CustomerID', 'OrderID', 'Order Date', 'ProductID', 'Returned', 'Quantity', 'Sales'))

store <- df %>%
  select(c('StoreID', 'Store', 'Store First Order')) %>%
  distinct() %>%
  rename('First Order' = 'Store First Order') %>%
  arrange(`StoreID`)

customer <- df %>%
  select(c('CustomerID', 'Customer', 'Return %', 'Number of Orders', 'Customer First Order')) %>%
  distinct() %>%
  rename('First Order' = 'Customer First Order') %>%
  arrange(`CustomerID`)
  
product <- df %>%
  select(c('ProductID', 'Category', 'Sub-Category', 'Product Name', 'Unit Price', 'Product First Sold')) %>%
  distinct() %>%
  rename('First Sold' = 'Product First Sold') %>%
  arrange(`ProductID`)

View(fact)
View(store)
View(customer)
View(product)
