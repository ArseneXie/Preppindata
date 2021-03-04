library(readxl)
library(dplyr)
library(tidyr)
library(stringr)
library(splitstackshape)

round_half_up <- function (x, digits=0){
  posneg = sign(x)
  z = trunc(abs(x) * 10 ^ (digits + 1)) / 10
  z = floor(z * posneg + 0.5) / 10 ^ digits
  return(z)
  }

final <- read_excel("F:/Data/Customer Information.xlsx") %>%
  cSplit(., 'IDs', ' ') %>%
  pivot_longer(everything(), names_to = c(".value",NA), names_pattern = '(ID)(.*)', values_drop_na=TRUE) %>%
  mutate('Phone' = str_extract(`ID`,'(\\d{6})(?=,)'),
         'Area Code Key' = str_extract(`ID`,'(?<=,)(\\d{2}[A-Z])'),
         'Product ID' = str_extract(`ID`,'([A-Z]+)$'),
         'Quantity' = as.integer(str_extract(`ID`,'(\\d+)(?=-)'))) %>%
  filter(`Quantity`>0) %>%
  merge(.,read_excel("F:/Data/Area Code Lookup.xlsx") %>%
          filter(!(`Area` %in% c('Clevedon', 'Fakenham', 'Stornoway'))) %>%
          mutate('Area Code Key' = paste0(str_sub(`Code`,-2),str_sub(`Area`,1,1))) %>%
          group_by(`Area Code Key`) %>%
          filter(n()==1), by='Area Code Key') %>%
  merge(.,read_excel("F:/Data/Product Lookup.xlsx") %>%
          mutate('Price' = as.numeric(str_sub(`Price`,2))), by='Product ID') %>%
  group_by(`Area`,`Product Name`) %>%
  summarise('Revenue' = round_half_up(sum(`Price`*`Quantity`)),
            .groups='drop') %>%
  group_by(`Area`) %>%
  mutate('Rank' = dense_rank(desc(`Revenue`)),
         '% of Total ¡V Product' = round_half_up(`Revenue`/sum(`Revenue`)*100,2)) %>%
  select(c('Rank', 'Area', 'Product Name', 'Revenue', '% of Total ¡V Product'))
 
View(final)
