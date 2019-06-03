library(dplyr)
library(readr)

jdata <- read_csv("E:/PD - JSON DATA Stock data.csv",
                  col_types = cols(JSON_Name = col_character(),
                                   JSON_ValueString = col_character())) %>%
  na.omit() 

final <- jdata %>%
  mutate('Category'= lapply(strsplit(`JSON_Name`, '\\.'), function(x) x[4])) %>%
  filter(`Category` != 'meta') %>%
  mutate('Row'= lapply(lapply(strsplit(`JSON_Name`, '\\.'),rev), function(x) x[1])) %>%
  mutate('DataType'= lapply(lapply(strsplit(`JSON_Name`, '\\.'),rev), function(x) x[2])) %>%
  select(c('Row','DataType','JSON_ValueString')) %>%
  spread('DataType', 'JSON_ValueString') %>%
  mutate('Date'=as.POSIXct(as.integer(`timestamp`), origin="1970-01-01",tz = "GMT")) %>%
  select(c('Date','volume','high','low','adjclose','close','open','Row'))

View(final)