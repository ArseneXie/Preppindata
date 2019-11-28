library(readxl)
library(dplyr)
library(tidyr)
library(stringr)

xls = "E:/Preppin Data Final 161119.xlsx"

order <- read_excel(path = xls,  sheet = "Complaints ") %>%
  mutate('Order Number' = str_extract(`Complaint`,'\\b(\\d{5})\\b'),
         'Customer ID' = str_extract(`Complaint`,'\\b(\\d{4})\\b'),
         'Item Number' = str_extract(`Complaint`,'\\b(\\d{1})\\b(?!\\sday)'),
         'Complaint Flag' = 1) %>%
  distinct(`Order Number`,`Customer ID`,`Item Number`,`Complaint Flag`) %>%
  merge(x = read_excel(path = xls,  sheet = "Orders"), y = .,
        by = c('Order Number','Customer ID','Item Number'), all.x = TRUE) %>%
  mutate_at(vars('Complaint Flag'), ~replace_na(., 0)) %>%
  merge(., read_excel(path = xls,  sheet = "Batches"),
        by = c('Batch Number','Product','Scent')) %>%
  group_by(`Batch Number`) %>%
  mutate('Refund Ratio' = sum(`Complaint Flag`)/n(),
         'Recall Batch' = if_else(`Refund Ratio`>=0.2,1,0))

lost <- order %>%
  summarise('Refund Items Only' = sum(`Price`*`Complaint Flag`*(1-`Recall Batch`)),
            'Recall Whole Batch' = max(`Price`*`Size of Order`*`Recall Batch`),
            'Total Amount Lost' = `Refund Items Only` + `Recall Whole Batch`) %>%
  gather(., key='Type of Refund', value='Money Lost', -'Batch Number', na.rm = TRUE) %>%
  group_by(`Type of Refund`) %>%
  summarise('Money Lost' = sum(`Money Lost`))

remain <- order %>%
  filter(`Recall Batch`== 0) %>%
  summarise('Batch Remain' = max(`Size of Order`) - n(),
            'Product' = max(`Product`),
            'Scent' = max(`Scent`)) %>%
  group_by(`Product`,`Scent`) %>%
  summarise('Stock Remaining' = sum(`Batch Remain`))
  
View(lost)
View(remain)