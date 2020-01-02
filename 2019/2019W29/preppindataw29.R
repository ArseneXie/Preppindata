library(readxl)
library(dplyr)
library(tidyr)
library(splitstackshape)
library(stringr)

subscript <- read_excel("E:/PD - Week 29 Input.xlsx", 
                       sheet = "Customers", col_types = c("text", 
                                                          "text", "text")) %>%
  cSplit(., 'Packages', '|') %>%
  gather(., key='var', value='Subscription Package', starts_with('Packages'),na.rm=TRUE) %>%
  select(-('var')) %>%
  merge(.,freq <- read_excel("E:/PD - Week 29 Input.xlsx", 
                             sheet = "Subscription Packages", col_types = c("text", 
                                                                            "text")) %>%
          mutate('Annum Freq' = case_when(`Frequency`=='week' ~ 52,
                                          `Frequency`=='month' ~ 12,
                                          `Frequency`=='quarter' ~ 4,
                                          TRUE ~ 1)) %>%
          select(-'Frequency') %>%
          rename('Frequency' = 'Subscription Package'), by='Frequency') %>%
  select(-'Frequency') %>%
  merge(.,pkgs <-  read_excel("E:/PD - Week 29 Input.xlsx", 
                              sheet = "Subscription Products", col_types = c("text", 
                                                                             "text", "numeric")) %>%
          mutate('Subscription Package'=str_extract(`Subscription Package`,'\\d+')),
        by='Subscription Package') %>%
  mutate('MPrice' = floor(weighted.mean(`Price`,if_else(`Product` != 'Mystery',`Annum Freq`,0))),
         'Price'= if_else(`Product` != 'Mystery',`Price`,`MPrice`))


final1 <- subscript %>%
  select(c('Subscription Package','Product','Price')) %>%
  distinct()

final2 <- subscript %>%
  group_by(`Name`) %>%
  summarise('Subscription Cost(Annum)'= sum(`Annum Freq`*`Price`))

View(final1)
View(final2)