library(readxl)
library(dplyr)

xlsx <- "C:/Data/PreppinData/PD 2022 Wk 19 Input.xlsx"

sales <- read_excel(xlsx, 'Sales') %>%
  merge(read_excel(xlsx, 'Size Table') %>% rename('Sales Size' = 'Size'), by.x='Size', by.y='Size ID') %>%
  merge(read_excel(xlsx, 'Product Set') %>%
          rename('Product Size' = 'Size') %>%
          mutate('Product' = gsub('S','',`Product Code`)), by='Product')
  
correct_sales <- sales %>%
  filter(`Sales Size`==`Product Size`) %>%
  select(c('Product Size', 'Scent', 'Product', 'Store'))

wrong_sales <- sales %>%
  filter(`Sales Size`!=`Product Size`) %>%
  group_by(`Product Code`, `Product Size`, `Scent`) %>%
  summarise('Number of Sales with wrong size' = n(), .groups='drop')
  
View(correct_sales)
View(wrong_sales)
