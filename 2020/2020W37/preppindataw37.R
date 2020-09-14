library(dplyr)
library(readxl)
library(tidyr)
library(lubridate)
library(bizdays)
library(fuzzyjoin)

Sys.setlocale("LC_ALL","English")

my_hol <- read_excel("F:/Data/Start Date.xlsx", sheet = "Holidays") %>%
  summarise('Holidays'= sum(`Holidays`)) %>%
  .[[1]]
tw_hol <-read_excel("F:/Data/Taiwan Holidays.xlsx", col_types = c("numeric", "text", "skip", "skip"))
start_date <- as.Date("2019/1/1")
to_date <- as.Date("2020/9/11")

tw_hol_list <- tw_hol %>%
  filter(grepl('.*to.*',`Date`)) %>%
  separate(`Date`,c('From Date', 'To Date'), sep=' to ') %>%
  mutate('From Date' = as.Date(paste(`From Date`,`Year`), format='%d %b %Y'),
         'To Date' = as.Date(paste(`To Date`,`Year`), format='%d %b %Y'),
         'Days' = time_length(`To Date` - `From Date`,unit='days'),
         'Max Days' = max(`Days`)->>maxseq) %>%
  fuzzy_inner_join(.,data.frame('Seq' =seq(0,maxseq)),
                   by = c('Days'='Seq'),
                   match_fun = list(`>=`)) %>%
  mutate('Date' = `From Date`  %m+% days(`Seq`)) %>% 
  select('Date') %>%
  rbind(.,tw_hol %>%
          filter(!grepl('.*to.*',`Date`)) %>%
          mutate('Date' = as.Date(as.numeric(`Date`),origin = "1899-12-30"),
                 'Excel Conv Year' = year(`Date`),
                 'Date' = `Date` %m+% years(`Year`-`Excel Conv Year`)) %>% 
          select('Date'))
 
cal <- create.calendar('mycal', holidays=pull(tw_hol_list, `Date`), 
                       weekdays=c("saturday", "sunday"),
                       start.date = start_date, end.date = to_date, financial=FALSE)

final <- data.frame('Start Date'=start_date, 'Today'=to_date,
                   'Working Days'= bizdays(start_date %m+% days(1),to_date,cal)-my_hol)

View(final)
