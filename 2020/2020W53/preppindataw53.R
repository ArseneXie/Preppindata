library(readr)
library(dplyr)
library(tidyr)
library(stringr)
library(lubridate)
library(fuzzyjoin)

Sys.setlocale("LC_ALL","English")

old_star <- read_csv("F:/Data/Old Star Signs.csv", col_names = FALSE)[1:2] %>%
  `colnames<-`(c('Old Star Sign', 'DateRange')) %>%
  rbind(.,read_csv("F:/Data/Old Star Signs.csv", col_names = FALSE)[3:4] %>%
          `colnames<-`(c('Old Star Sign', 'DateRange'))) %>%
  rbind(.,read_csv("F:/Data/Old Star Signs.csv", col_names = FALSE)[5:6] %>%
          `colnames<-`(c('Old Star Sign', 'DateRange'))) %>%
  drop_na() %>%
  mutate('Begin Date' = as.Date(paste0('2020/',str_extract(`DateRange`, '^(\\d+/\\d+)'))),
         'End Date' = as.Date(paste0('2020/',str_extract(`DateRange`, '(\\d+/\\d+)$'))),
         'End Date' =  `End Date` %m+% years(ifelse(`End Date`<`Begin Date`,1,0)))

new_star <- read_csv("F:/Data/New Star Signs.csv", col_names = FALSE) %>%
  mutate('New Star Sign' = str_extract(`X1`, '^(\\w+)'),
         'From Date' = as.Date(paste0('2020 ',str_replace(`X1`, '.*:\\s(\\w{3})\\w*\\s(\\d+).*','\\1 \\2')),"%Y %b %d"),
         'To Date' = as.Date(paste0('2020 ',str_replace(`X1`, '.*\\s(\\w{3})\\w*\\s(\\d+)$','\\1 \\2')),"%Y %b %d"),
         'To Date' =  `To Date` %m+% years(ifelse(`To Date`<`From Date`,1,0)),
         'Date Range' = paste(str_replace(`X1`, '.*:\\s(\\w{3})\\w*\\s(\\d+).*','\\2 \\1'),'-',
                              str_replace(`X1`, '.*\\s(\\w{3})\\w*\\s(\\d+)$','\\2 \\1'))) 

all_date = read_csv("F:/Data/Scaffold.csv", col_types = cols(Date = col_date(format = "%d/%m/%Y"))) %>%
  mutate('Birthday' = format(`Date`,'%b %d'))


final <- merge(fuzzy_inner_join(all_date, old_star, 
                                by = c('Date'='Begin Date','Date'='End Date'), match_fun = list(`>=`, `<=`)),
               fuzzy_inner_join(all_date, new_star, 
                                by = c('Date'='From Date','Date'='To Date'), match_fun = list(`>=`, `<=`)),
               by='Birthday') %>%
  group_by(`Birthday`) %>%
  mutate('The Same' = ifelse(`Old Star Sign`==`New Star Sign`,1,0),
         'The Same Cases' = max(`The Same`)) %>%
  filter(`The Same Cases`==0) %>%
  select(c('Birthday', 'Old Star Sign', 'New Star Sign', 'Date Range'))

View(final)
