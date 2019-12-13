library(readxl)
library(dplyr)
library(tidyr)
library(stringr)
library(fuzzyjoin)

xls = "E:/PD - Wk 43 - Next Year's Store Targets-2.xlsx"

actions <- read_excel(path = xls, sheet = 'Targets - Next steps') %>%
  rename('Target' = !!names(.[1]),
         'Actions' = !!names(.[3])) %>%
  mutate('Range' = if_else(as.integer(`Range`)==1,'100%',`Range`, `Range`), 
         'Range From' = as.integer(str_extract(`Range`,'^(\\d+)')),
         'Range To' = as.integer(str_extract(`Range`,'\\d+(?=%$)'))) %>%
  mutate_at(vars('Range From'), ~replace_na(., 0)) %>%
  mutate_at(vars('Range To'), ~replace_na(., 9999)) %>%
  select(c('Target','Actions','Range From','Range To'))

final <- read_excel(path = xls, sheet = 'Monthly Sales Value') %>%
  filter(`Store`!='Total') %>%
  gather(., key='Month', value='Sales', starts_with('Month'),na.rm=TRUE) %>%
  mutate('Quarter' = (as.integer(str_extract(`Month`,'\\s(\\d+)\\s'))-1)%/%3+1) %>%
  group_by(`Store`,`Quarter`) %>%
  summarise('Sales' = sum(`Sales`)) %>%
  merge(., read_excel(path = xls, sheet = 'Quarterly Store Targets') %>%
          gather(., key='Quarter', value='Target Value', starts_with('Q'),na.rm=TRUE) %>%
          mutate('Quarter'=as.integer(str_extract(`Quarter`,'\\d+'))),
        by.x = c('Store','Quarter'), by.y = c('Location','Quarter')) %>%
  mutate('Variance to Target' = `Sales` - `Target Value`,
         'Variance to Target %' = round(`Sales`/`Target Value`*100)) %>%
  fuzzy_inner_join(.,actions,
                   by=c('Variance to Target %' = 'Range From','Variance to Target %' = 'Range To'),
                   match_fun = list(`>=`,`<=`)) %>%
  select(c('Store', 'Variance to Target', 'Variance to Target %', 'Sales', 'Target Value',
           'Quarter', 'Region', 'Target', 'Actions'))
  
View(final)  