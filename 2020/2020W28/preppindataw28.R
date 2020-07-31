library(dplyr)
library(readxl)
library(tidyr)
library(stringr)

xlsx <- "F:/Data/PD Olympics.xlsx"
Sys.setlocale("LC_ALL","English")

final <- read_excel(xlsx) %>%
  drop_na(`Dates`) %>%
  select(c('Games', 'Host', 'Dates', 'Nations', 'Sports', 'Events')) %>%
  mutate('Start Date' = as.Date(paste(1896+4*(as.numeric(as.roman(`Games`))-1),
                                      str_extract(`Dates`,'([A-Za-z]+)'),
                                      str_extract(`Dates`,'(\\d+)(?=\\D+\\d+)'),sep='-'),
                                format = '%Y-%B-%d'),
         'End Date' = as.Date(paste(1896+4*(as.numeric(as.roman(`Games`))-1),
                              str_extract(`Dates`,'([A-Za-z]+)$'),
                              str_extract(`Dates`,'(\\d+)(?=\\D+$)'),sep='-'),
                              format = '%Y-%B-%d')) %>%
  select(c('Start Date', 'End Date','Games', 'Host', 'Nations', 'Sports', 'Events'))
  
View(final)