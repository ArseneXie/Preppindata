library(dplyr)
library(readr)
library(stringr)

Sys.setlocale("LC_ALL","English")

txndata <- read_csv("C:/Data/PreppinData/PD 2023 Wk 1 Input.csv", 
                  col_types = cols(`Transaction Date` = col_date(format = "%d/%m/%Y %H:%M:%S"))) %>%
  mutate('Bank' = str_extract(`Transaction Code`,'^([A-Z]+)'),
         'Online or In-Person' = if_else(`Online or In-Person`==1, 'In-Person', 'Online'),
         'Transaction Date' = strftime(`Transaction Date`, '%A'))

out1 <- txndata %>%
  group_by(`Bank`) %>%
  summarise('Value'=sum(`Value`), .groups='drop')

out2 <- txndata %>%
  group_by(`Bank`, `Online or In-Person`, `Transaction Date`) %>%
  summarise('Value'=sum(`Value`), .groups='drop')

out3 <- txndata %>%
  group_by(`Bank`, `Customer Code`) %>%
  summarise('Value'=sum(`Value`), .groups='drop')
  
View(out1)
View(out2)
View(out3)