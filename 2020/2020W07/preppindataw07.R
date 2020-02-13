library(dplyr)
library(readr)
library(stringr)
library(lubridate)
library(fuzzyjoin)

report_date <- read_csv("E:/PD 2020 Wk 7 Reporting Date Input.csv", 
                        col_types = cols(Month = col_date(format = "%b-%Y"))) %>%
  mutate('Join Before' = `Month`+ months(1) - days(1),
         'Leave After' = `Month`+ months(1))

final <- rbind(read_csv("E:/PD 2020 Wk 7 Current Employees Input.csv", 
                        col_types = cols(`Join Date` = col_date(format = "%m/%d/%Y"))) %>%
                 mutate('Salary' = as.numeric(str_remove(gsub(',','',`Salary`),'\\D')),
                        'Leave Date' = max(report_date$`Leave After`)),
               read_csv("E:/PD 2020 Wk 7 Leavers Input.csv", 
                        col_types = cols(`Join Date` = col_date(format = "%m/%d/%Y"), 
                                         `Leave Date` = col_date(format = "%m/%d/%Y")))) %>%
  fuzzy_inner_join(.,report_date,
                   by=c('Join Date'='Join Before','Leave Date'='Leave After'),
                   match_fun=list(`<=`,`>=`)) %>%
  group_by(`Month`) %>%
  summarise('Total Monthly Salary' = sum(`Salary`),
            'Current Employees' = n(),
            'Avg Salary per Current Employees' = mean(`Salary`))

View(final)