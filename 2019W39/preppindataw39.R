library(dplyr)
library(tidyr)
library(readxl)
library(stringr)
library(purrr)

input <- "E:/PD Wk 39 .xlsx"

final <-  input %>%
  excel_sheets() %>%
  set_names() %>%
  map_df(
    ~ read_excel(path = input, sheet = .x, col_types = c('text','text')),
    .id = 'Sheet Name') %>%
  mutate('TimeType'=str_extract(`Sheet Name`,'^(\\w+\\s\\w+)'),
         'EntryType'=str_replace(`Sheet Name`,'^(\\w+\\s\\w+\\s)',''),
         'Pageviews %'=str_replace(str_extract(`Pageviews`,'(?<=\\()(.*)(?=%)'),'<1','0.5'),
         'Pageviews Value'= str_extract(`Pageviews`,'^(\\d+)')) %>%
  group_by(`TimeType`,`EntryType`) %>%
  mutate('Missing %' = as.integer(as.integer(`Pageviews Value`)/sum(as.integer(`Pageviews Value`))*100),
         'Pageviews %'= ifelse(is.na(`Pageviews %`),as.character(`Missing %`),`Pageviews %`)) %>%
  select(c('EntryType','TimeType','Entry','Pageviews %','Pageviews Value')) %>%
  gather(., key='ValType', value='R2CVal', contains('Pageviews')) %>%
  mutate_at(vars('R2CVal'),as.numeric) %>%
  unite('R2CCol', c('TimeType', 'ValType'), sep = ' ', remove = TRUE) %>%
  spread(`R2CCol`,`R2CVal`) %>%
  mutate('Change in % This Month' = `This Month Pageviews %` - `All Time Pageviews %`) %>%
  arrange(desc(`This Month Pageviews Value`)) %>%
  ungroup()
  
browser_output <- final %>% filter(`EntryType`=='Browsers') %>% select(-'EntryType')
origin_output <- final %>% filter(`EntryType`=='Origin') %>% select(-'EntryType')
os_output <- final %>% filter(`EntryType`=='Operating System') %>% select(-'EntryType')

View(browser_output)
View(origin_output)
View(os_output)