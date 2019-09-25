library(readxl)
library(dplyr)
library(tidyr)
library(splitstackshape)

sales <- read_excel("E:/PD Wk 32 Input.xlsx", 
                    col_types = c("text", "text", "text", 
                                  "text", "text", "text")) %>%
  rename('Sales 1' = !!names(.[4]),
         'Sales 2' = !!names(.[6])) %>%
  cSplit(., 'Address', ',') %>%
  rename('Property Number' = 'Address_1',
         'Town' = 'Address_2',
         'Postal Code' = 'Address_3',
         'Country' = 'Address_4') %>%
  mutate('Property Number' = as.integer(gsub('[^0-9]','',`Property Number`))) %>%
  mutate_at(vars(matches('Product')), ~gsub('-',' ',.)) %>%
  unite('ProdSales_1',`Product 1`,`Sales 1`,sep='/') %>%
  unite('ProdSales_2',`Product 2`,`Sales 2`,sep='/') %>%
  gather(., key='ToDrop', value='ToSplit', starts_with('ProdSales_'),na.rm=TRUE) %>%
  separate(`ToSplit`, c('Product', 'Sales'), sep = '/') %>%
  mutate_at(vars('Sales'), ~as.integer(.)) %>%
  select(-'ToDrop')

View(sales)