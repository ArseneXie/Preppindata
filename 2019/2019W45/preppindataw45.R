library(dplyr)
library(readr)
library(purrr)
library(stringr)

rowdata <- dir("E:/InputW45/", pattern = "\\w+\\s\\w+\\.csv") %>%
  map(~ read_csv(file.path("E:/InputW45/", .),col_types =cols(`Scent` = col_character(),
                                                              `Sales Value` = col_double(),
                                                              `Sales Volume` = col_double())) 
      %>% mutate('Dummy'=.x,'Store' = str_extract(.x,'^(\\w+)'),
                 'Weekday' = str_extract(.x,'(\\w+)(?=\\.)'))) %>%
  reduce(rbind) %>%
  distinct() %>%
  merge(., read_csv("E:/InputW45/Dates.csv",col_types =cols(`Dates` = col_character())) %>%
          mutate('Weekday' = str_extract(`Dates`,'^(\\w+)')), on='Weekday')
  
final1 <- rowdata %>%
  group_by(`Store`,`Scent`) %>%
  summarise('Sales Volume' = sum(`Sales Volume`),
            'Sales Value' = sum(`Sales Value`)) %>%
  group_by(`Store`) %>%
  mutate('Scent % of Store Sales Volumes' = round(`Sales Volume`/sum(`Sales Volume`),2),
         'Scent % of Store Sales Values' = round(`Sales Value`/sum(`Sales Value`),2)) %>%
  select(-c('Sales Volume','Sales Value'))

final2 <- rowdata %>%
  group_by(`Store`,`Dates`) %>%
  summarise('Sales Volume' = sum(`Sales Volume`),
            'Sales Value' = sum(`Sales Value`)) %>%
  group_by(`Store`) %>%
  mutate('Weekday % of Store Sales Volumes' = round(`Sales Volume`/sum(`Sales Volume`),2),
         'Weekday % of Store Sales Values' = round(`Sales Value`/sum(`Sales Value`),2)) %>%
  select(-c('Sales Volume','Sales Value'))

View(final1)
View(final2)
