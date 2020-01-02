library(readxl)
library(dplyr)
library(stringr)
library(lubridate)
library(purrr)

input <- "E:/PD - Week 23.xlsx"
sheets <- excel_sheets(input)

final <-  input %>%
  excel_sheets() %>%
  set_names() %>%
  map_df(
    ~ read_excel(path = input, sheet = .x,),
    .id = "sheet name") %>%
  mutate('Start Date'= parse_date_time(paste(str_extract(`sheet name`,'(?<=wc\\s).*'),
                                             '2019'),'dbY')) %>%
  mutate('Date' = `Start Date` %m+% days(case_when(`Day`== 'Monday' ~ 0,
                                                `Day`== 'Tuesday' ~ 1,
                                                `Day`== 'Wednesday' ~ 2,
                                                `Day`== 'Thursday' ~ 3,
                                                `Day`== 'Friday' ~ 4,
                                                `Day`== 'Saturday' ~ 5,
                                                TRUE ~ 6)),
         'Notes'= str_to_title(`Notes`),
         'Name' = str_extract(`Notes`,'.*(?=\\sWant)'),
         'Value' = as.integer(str_extract(`Notes`,'(?<=\\s\\D)\\d+')),
         'Scent' = str_extract(`Notes`,'\\w+(?=\\s\\w+\\s\\w+$)'),
         'Product' = str_extract(`Notes`,'\\w+\\s\\w+$'),
         'Notes'= tolower(`Notes`)) %>%
  select(c('Date','Name','Value','Scent','Product','Notes'))

View(final)