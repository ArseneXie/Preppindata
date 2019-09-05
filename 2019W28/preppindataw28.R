library(readxl)
library(dplyr)
library(tidyr)
library(stringr)
library(lubridate)

xlsx <- 'E:/PD Week 28 Input.xlsx'

data_head <- read_excel(xlsx, col_names = FALSE, n_max = 2) %>%
  mutate('col_level' = row_number()) %>%
  gather(., key='var', value='cols', -'col_level') %>%
  group_by(`col_level`) %>% 
  fill(`cols`) %>%
  spread(.,`col_level`, `cols`) %>%
  mutate('col_name' = ifelse(is.na(`2`),`1`,paste0(`1`,'-',`2`))) %>%
  arrange(as.integer(str_extract(`var`,'\\d+')))

final <- read_excel(xlsx, skip = 2 ,col_names = FALSE) %>%
  rename_all(funs(data_head[['col_name']][as.integer(str_extract(.,'\\d+'))])) %>%
  group_by(`Employee`) %>%
  arrange(`Observation Interval`) %>%
  mutate('Accum Length (mins)' = cumsum(`Observation Length (mins)`),
         'Observation Start Time' = dmy_hms(paste(str_extract(excel_sheets(xlsx)[1],'(\\d+\\.*)+'),
                                                  format(`Observation Start Time`,'%H:%M:%S'))) 
         %m+% minutes(x = `Accum Length (mins)`-`Observation Length (mins)`)) %>%
  ungroup() %>%
  gather(., key='Type Name', value='Type Value', contains('-'), na.rm = TRUE) %>%
  select(-c('Accum Length (mins)','Type Value')) %>%
  separate(`Type Name`, c('Real Col Name', 'Real Col Value'), sep = '-') %>%
  spread(.,`Real Col Name`, `Real Col Value`) %>%
  rename('Interaction' = 'Interaction With')

View(final)