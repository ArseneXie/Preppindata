library(dplyr)
library(readr)
library(tidyr)
library(stringr)
library(splitstackshape)

Sys.setlocale("LC_ALL","English")

final <- read_csv("F:/Data/Battles Input.csv") %>%
  mutate('DownloadData' = str_replace_all(`DownloadData`,'<br />','#@')) %>%
  cSplit(., 'DownloadData', '#@') %>%
  drop_na() %>%
  `colnames<-`(c('ToDrop', 'Battle', 'Date', 'War', 'Victors', 'Description')) %>%
  select(-c('ToDrop')) %>%
  mutate('Battle' = str_remove(`Battle`,'<.*>'),
         'Victors' = str_remove(`Battle`,'<.*>(Victors:\\s)*'),
         'Date' = as.Date(str_replace(str_replace(str_replace(
           str_remove(`Date`,'\\D+$'),'^(\\D+)\\s(\\d+)\\D','\\2 \\1,'),
           '^(\\d+)\\W+\\d*\\s*(\\w+)\\W*(\\d+)','\\1 \\2, \\3'),
           '^(\\d+)$', '1 January, \\1'),format="%d %B, %Y")) 

View(final)