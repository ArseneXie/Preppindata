library(dplyr)
library(readr)
library(stringr)
library(lubridate)

df <- read_csv("F:/Data/PD 2021 Wk 2 Input - Bike Model Sales.csv", 
                  col_types = cols(`Order Date` = col_date(format = "%d/%m/%Y"),
                                   `Shipping Date` = col_date(format = "%d/%m/%Y"))) %>%
  mutate('Brand' = str_remove_all(`Model`,'[^A-Z]'),
         'Order Value' = `Quantity`*`Value per Bike`,
         'Days to Ship' = time_length(`Shipping Date`-`Order Date`,'day'))

finalA <- df %>%
  group_by(`Brand`,`Bike Type`) %>%
  summarise('Quantity Sold' = sum(`Quantity`),
            'Order Value' = sum(`Order Value`),
            'Avg Bike Value per Brand' = round(mean(`Value per Bike`),1))
  
finalB <- df %>%
  group_by(`Brand`,`Store`) %>%
  summarise('Total Quantity Sold' = sum(`Quantity`),
            'Total Order Value' = sum(`Order Value`),
            'Avg Days to Ship' = round(mean(`Days to Ship`),1))

View(finalA)
View(finalB)
