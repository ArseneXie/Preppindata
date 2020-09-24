library(dplyr)
library(readxl)
library(tidyr)
library(stringr)
library(splitstackshape)

final <- read_excel("F:/Data/2020W39 Input.xlsx", sheet = "Orders") %>%
  pivot_longer(.,cols=-'Person', names_to='Weekday', values_to='Order Item' ,values_drop_na=TRUE) %>%
  mutate('Order Item' = str_replace_all(`Order Item`,'\\s+with\\s+',',')) %>%
  cSplit(., 'Order Item', ',') %>%
  pivot_longer(.,cols=starts_with('Order Item'), names_to='ToDrop', values_to='Order Item' ,values_drop_na=TRUE) %>%
  mutate('Item Key' = str_remove_all(tolower(`Order Item`),'\\s*(tea|(fruit )*smoothie)$')) %>%
  merge(., read_excel("F:/Data/2020W39 Input.xlsx", sheet = "Price List") %>%
          pivot_longer(.,cols=-ends_with('Price'), names_to='Type', values_to='Item' ,values_drop_na=TRUE) %>%
          pivot_longer(.,cols=ends_with('Price'), names_to='Price Type', values_to='Price' ,values_drop_na=TRUE) %>%
          filter(`Price Type`==paste(`Type`,'Price')) %>%
          mutate('Item Key' = str_remove_all(tolower(`Item`),'\\s*(tea|(fruit )*smoothie)$')),
        by='Item Key') %>%
  group_by(`Person`) %>%
  summarise('Monthly Spend' = sum(`Price`)*4,
            'Potential Savings' = `Monthly Spend`-20,
            'Worthwhile?' = (`Potential Savings`>=0))

View(final)
