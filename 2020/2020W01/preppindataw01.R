library(dplyr)
library(readr)
library(stringr)
library(zoo)

final <- read_csv("E:/PD 2020 WK 1 Input - Sheet1.csv", col_types=cols(Item = col_character(),
                                                                       Profit = col_double())) %>%
  mutate('LV1' = str_extract(`Item`,'^(\\d+)'),
         'LV2' = str_extract(`Item`,'(?<=\\.)(\\d+)(?=(\\.|\\s))'),
         'LV3' = str_extract(str_extract(`Item`,'(?:\\d+\\.){2}(\\d+)'),'\\d+$'),
         'Level' = if_else(is.na(`LV2`),1,if_else(is.na(`LV3`),2,3)),
         'Item' = paste0(strrep(' ',(`Level`-1)*5),`Item`)) %>%
  group_by(`LV1`) %>%
  mutate_at('Profit', na.aggregate, FUN = sum) %>%
  mutate('Profit' = if_else(`Level`==2,NA_real_,`Profit`)) %>%
  group_by(`LV1`,`LV2`) %>%
  mutate_at('Profit', na.aggregate, FUN = sum) %>%
  ungroup() %>%
  select(c('Item','Profit'))

View(final)