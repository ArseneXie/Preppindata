library(readxl)
library(dplyr)
library(fuzzyjoin)
library(lubridate)

autolog <- read_excel("E:/PD12 - System errors.xlsx", 
                      sheet = "Automatic Error log", col_types = c("date", 
                                                                   "date", "text", "text")) %>%
  mutate('StartDateTime'= `Start Date / Time` %m+% minutes(-30),
         'EndDateTime'= `End Date / Time` %m+% minutes(30))
  
manlog <- read_excel("E:/PD12 - System errors.xlsx", 
                     sheet = "Manual capture error list", 
                     col_types = c("date", "date", "date", 
                                   "date", "text", "text")) %>%
  mutate('StartDateTime'= as_datetime(paste(strftime(`Start Date`, format="%Y-%m-%d"),
                                        strftime(`Start Time`, format="%H:%M:%S", tz = "UTC"))),
         'EndDateTime'= as_datetime(paste(strftime(`End Date`, format="%Y-%m-%d"),
                                            strftime(`End Time`, format="%H:%M:%S", tz = "UTC")))) %>%
  select(c('System','Error','StartDateTime','EndDateTime'))


final <- fuzzy_full_join(autolog, manlog, 
                        by = c('System','StartDateTime','EndDateTime'),
                        match_fun = list(`==`, `<=`, `>=`)
                        ) %>%
  mutate('Start Date / Time'= as_datetime(ifelse(is.na(`Start Date / Time`),`StartDateTime.y`,`Start Date / Time`)),
         'End Date / Time'= as_datetime(ifelse(is.na(`End Date / Time`),`EndDateTime.y`,`End Date / Time`)),
         'System' = ifelse(is.na(`System.x`),`System.y`,`System.x`),
         'Error Source' = ifelse(is.na(`System.x`),'Manual capture error list','Automatic Error log'),
         'Error'= ifelse(is.na(`Error.x`),`Error.y`,`Error.x`)) %>%
  select(c('System','Error','Error Source','Start Date / Time','End Date / Time')) %>%
  mutate('Downtime in Hours'= as.numeric((`End Date / Time` - `Start Date / Time`)/60)) %>%
  group_by(`System`) %>%
  mutate('Total Downtime in Hours' = sum(`Downtime in Hours`),
         '% of system downtime'= `Downtime in Hours` / sum(`Downtime in Hours`))
  
View(final)
