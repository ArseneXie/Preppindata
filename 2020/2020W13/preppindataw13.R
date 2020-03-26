library(dplyr)
library(readxl)
library(stringr)

xlsx <- "E:/PD week 12 input.xlsx"

final <- read_excel(xlsx, sheet = "Percentage of Sales") %>%
  filter(`Percentage of Sales`>0) %>%
  mutate('Product' = paste0(`Product ID`,`Size`),
         'Year Week Number' = paste0(strftime(`Week Commencing`,format = '%Y'),
                                     str_pad(as.integer(strftime(`Week Commencing`,format = '%U'))+1, 2, pad = '0'))) %>%
  merge(.,read_excel(xlsx,sheet = "Lookup Table") %>%
          mutate('ScentKey' = str_remove_all(tolower(`Scent`),'[^a-z]')), by='Product') %>%
  merge(.,read_excel(xlsx,sheet = "Total Sales") %>%
          mutate('ScentKey' = str_remove_all(tolower(`Scent`),'[^a-z]')) %>%
          select(-'Scent'), by=c('ScentKey','Year Week Number')) %>%
  mutate('Sales' = round(`Total Scent Sales`*`Percentage of Sales`,2)) %>%
  select(c('Year Week Number', 'Scent', 'Size', 'Product Type', 'Sales'))

View(final)
