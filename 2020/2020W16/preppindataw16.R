library(dplyr)
library(readxl)
library(splitstackshape)
library(arules)
library(stringr)

items <- read_excel('E:/Transactions.xlsx', sheet = 1) %>%
  select('Items') %>%
  cSplit_e(., 'Items', ',', drop = TRUE, type = 'character', fill=0) %>%
  rename_all(.funs = funs(sub('Items_','', .)))

rules <- apriori(as.matrix(items), parameter = list(supp = 0.001, conf = 0.01))

sup <- inspect(subset(rules, subset = size(lhs)==0)) %>%
  select(c('rhs','support')) %>% 
  mutate('lhs'=`rhs`,
         'LHS Support'=`support`,
         'RHS Support'=`support`) %>%
  select(-'support') 

final <- inspect(subset(rules, subset = size(lhs)==1 & size(rhs)==1)) %>%
  select(c('lhs','rhs','confidence','lift')) %>%
  merge(.,sup %>% select(c('rhs','RHS Support')), by='rhs') %>%
  merge(.,sup %>% select(c('lhs','LHS Support')), by='lhs') %>%
  mutate_if(is.factor, as.character) %>%
  mutate('LHS Item' = str_extract(`lhs`,'(?<=\\{)(.*)(?=\\})'),
         'RHS Item' = str_extract(`rhs`,'(?<=\\{)(.*)(?=\\})'),
         'Association Rule' = paste(`LHS Item`,'-->',`RHS Item`)) %>%
  select(c('Association Rule','LHS Item', 'RHS Item', 'LHS Support', 'RHS Support','confidence', 'lift'))

View(final)