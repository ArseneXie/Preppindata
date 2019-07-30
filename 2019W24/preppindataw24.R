library(readxl)
library(dplyr)
library(stringr)
library(lubridate)

final <- read_excel("E:/Messages Input.xlsx", 
                   sheet = "chat") %>%
  mutate('Name' = str_extract(`Field_1`,'([:alpha:]+\\s*)+(?=\\W)'),
         'Message' = str_extract(`Field_1`,'(?<=:\\s).*'),
         'Number of Words' = sapply(strsplit(`Message`,' '),length),
         'Date' = parse_date_time(str_extract(`Field_1`,'\\d+/\\d+/\\d+'),'d/m/Y'),
         'Hour' = as.integer(str_extract(`Field_1`,'(?<=\\s)\\d+(?=:)'))) %>%
  merge(.,calendar <- read_excel("E:/Dates Input.xlsx", 
                                 sheet = "Dates") %>%
          mutate('Date'= parse_date_time(paste(`Date`,'2019'),'d b Y')), by='Date') %>%
  mutate('Send from work' = ifelse(`Holiday?`=='Weekday' &
                                      ((`Hour`>=9 & `Hour`<12) | (`Hour`>13 & `Hour`<17)),1,0)) %>%
  group_by(`Name`) %>%
  summarise('Text' = n(),
            'Avg Words/Sentence'=mean(`Number of Words`),
            'Number of Words'=sum(`Number of Words`),
            'Text While at Work'=sum(`Send from work`),
            '% Send from Work'=mean(`Send from work`)*100)

View(final)