library(dplyr)
library(readxl)
library(tidyr)
library(purrr)
library(stringr)

input <- "E:/Can't Desktop Prep this-2.xlsx"

final <- input %>%
  excel_sheets() %>% .[grepl('.*Sales$',.)] %>%
  set_names() %>%
  map_df(
    ~ read_excel(path = input, sheet = .x),
    .id = 'Store') %>%
  mutate('Store' = str_extract(`Store`,'(.*)(?=\\s)')) %>%
  pivot_longer(., cols=matches('^(Sales|Profit)'), names_to='Col', values_to='Value') %>%
  separate(`Col`,c('Measure','Date'), sep=' ') %>%
  mutate('Date' = as.Date(`Date`, format='%d/%m/%Y')) %>%
  pivot_wider(., names_from=`Measure`, values_from=`Value`) %>%
  merge(., read_excel(input, 'Staff days worked') %>%
          pivot_longer(., cols=matches('[^(Month)]'), names_to='Store', values_to='Staff days worked'),
        by.x=c('Store','Date'), by.y=c('Store','Month')) %>%
  select(c('Store', 'Category', 'Scent', 'Date', 'Sales', 'Profit', 'Staff days worked'))

View(final)