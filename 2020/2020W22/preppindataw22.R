library(dplyr)
library(readxl)
library(tidyr)

xlsx <- "F:/Data/2020W22 Input.xlsx"

ttl <- read_excel(xlsx, sheet = "Total Market") 
comp <- read_excel(xlsx, sheet = "Companies") 
scent <- read_excel(xlsx, sheet = "Scents") 

march_ttl <- ttl$'March Sales'[1]
april_ttl <- march_ttl*(1+ttl$'Growth'[1])

final <- comp %>%
  rowwise() %>%
  mutate('random1' = runif(1), 
         'random2' = runif(1)) %>%
  ungroup() %>%
  mutate('March' = march_ttl*`random1`/ sum(`random1`),
         'ChangeBps' = -30+rank(desc(as.numeric(`random2`)))*10,
         'April' = april_ttl*(`random1`/ sum(`random1`)+`ChangeBps`/10000)) %>%
  select(c('Company','March','April')) %>%
  pivot_longer(., cols=matches('^(March|April)'), names_to='Month', values_to='CM Sales') %>%
  merge(scent, all=TRUE) %>%
  rowwise() %>%
  mutate('random1' = runif(1)) %>%
  ungroup() %>%
  group_by(`Company`,`Month`) %>%
  mutate('Sales' = `CM Sales`*`random1`/sum(`random1`)) %>%
  arrange(`Company`,`Month`) %>%
  select(c('Company', 'Month', 'Soap Scent', 'Sales'))

View(final)