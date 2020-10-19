library(dplyr)
library(tidyr)
library(readxl)
library(lubridate)

period <- data.frame(`Today` = as.Date('2020-10-09',format='%Y-%m-%d')) %>%
  mutate('Week' = as.integer(strftime(`Today`,format = '%U')),
         'Days' = as.integer(strftime(`Today`,format = '%w'))) %>%
  merge(data.frame(`Offset` = seq(0, -1))) %>%
  mutate('Category' = if_else(`Offset`==0,'This Year','Last Year'),
         'Year' = as.integer(strftime(`Today`,format = '%Y'))+`Offset`,
         'End Date' = as.Date(paste(`Year`,`Week`,`Days`),format='%Y %U %w'),
         'WTD' = floor_date(`End Date`, 'weeks'),
         'MTD' = floor_date(`End Date`, 'months'),
         'YTD' = floor_date(`End Date`, 'years')) %>%
  select(-c('Today','Week','Days','Offset')) %>%
  pivot_longer(.,cols=ends_with('TD'), names_to='Time Period', values_to='Start Date')

txn <- read_excel('F:/Data/Transactions.xlsx') %>%
  filter(`TransactionDate` >= period %>% summarise('min'= min(`Start Date`)) %>% .[[1]]) %>%
  mutate('From Date' = as.Date(`TransactionDate`),
         'To Date' = as.Date(`TransactionDate`),
         'Year' = as.integer(strftime(`TransactionDate`,format = '%Y')),
         'Source' = 'Transaction') %>%
  select(c('Year', 'From Date', 'To Date', 'ProductName', 'Quantity', 'Income', 'Source'))

target <- read_excel('F:/Data/Targets.xlsx') %>%
  rename('Quantity' = 'Quantity Target',
         'Income' = 'Income Target') %>%
  mutate('From Date'= floor_date(as.Date(paste0(`Year`,'-01-01'),format='%Y-%m-%d'),'weeks')+(`Week`-1)*7,
         'To Date' = `From Date`+6,
         'Source' = 'Target') %>%
  select(-'Week')

final <- rbind(txn, target) %>%
  merge(., period, by='Year') %>%
  filter((`From Date`>=`Start Date` & `To Date`<=`End Date`) | (`From Date`<=`End Date` & `To Date`>=`Start Date`)) %>%
  rowwise() %>%
  mutate('Category' = if_else(`Source`=='Transaction',`Category`,`Source`),
         'Modifier' = as.integer(difftime(min(`End Date`,`To Date`),max(`Start Date`,`From Date`), units='day'))+1) %>%
  ungroup() %>%
  select(c('ProductName', 'Category', 'Time Period', 'Modifier', 'Quantity', 'Income')) %>%
  pivot_longer(.,cols=c('Quantity', 'Income'), names_to='Metric', values_to='Value') %>%
  group_by(`ProductName`,`Category`, `Time Period`, `Metric`) %>%
  summarise('Value' = round(sum(if_else(`Category`=='Target',`Value`/7*`Modifier`,`Value`)))) %>%
  pivot_wider(., names_from='Category', values_from='Value', values_fn=list(`Value`=sum)) %>%
  mutate('% Differece to Last Year' = round(((`This Year`-`Last Year`)/`Last Year`),2),
         '% Differece to Target' = round(((`This Year`-`Target`)/`Target`),2)) %>%
  select(c('ProductName', 'Metric', 'Time Period', 'This Year', 'Last Year', 'Target', '% Differece to Last Year', '% Differece to Target'))
  
View(final)