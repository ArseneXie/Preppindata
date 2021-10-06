library(readxl)
library(dplyr)
library(tidyr)

input <- "F:/Data/Trend Input.xlsx"

final <- read_excel(path = input, sheet = 'Timeline', skip = 2) %>%
  pivot_longer(cols=-'Week', names_to='Search Term', names_pattern='([\\w\\s]+):.*', values_to='Index') %>%
  group_by(`Search Term`) %>%
  mutate('Avg Index' = round(mean(`Index`),1),
         'Index Peak' = max(`Index`),
         'First Peak' = min(if_else(`Index Peak`==`Index`,`Week`,NULL), na.rm=TRUE),
         'Year' = if_else(as.numeric(format(`Week`, '%m'))>=9,
                          as.numeric(format(`Week`, '%Y'))+1, as.numeric(format(`Week`, '%Y'))),
         'YearMeasure' = paste0(`Year`-1,'/',`Year`%%100,' avg index')) %>%
  filter(`Year`>= max(`Year`)-1) %>%
  select(-c('Week', 'Year')) %>%
  pivot_wider(names_from='YearMeasure', values_from='Index', values_fn = list(Index = mean)) %>%
  mutate('Status' = if_else(`2020/21 avg index`>=`2019/20 avg index`, 'Still Trendy', 'Lockdown Fad'),
         '2020/21 avg index' = round(`2020/21 avg index`,1)) %>%
  merge(., read_excel(path = input, sheet = 'Country Breakdown', skip = 2) %>%
          drop_na() %>%
          pivot_longer(cols=-'Country', names_to='Search Term', names_pattern='([\\w\\s]+):.*', values_to='Percentage') %>%
          group_by(`Search Term`) %>%
          filter(`Percentage`==max(`Percentage`)), by='Search Term') %>%
  rename('Country with highest percentage'='Country') %>%
  select(c('Search Term', 'Status', '2020/21 avg index', 'Avg Index', 'Index Peak', 'First Peak', 'Country with highest percentage'))

View(final)
