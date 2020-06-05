library(dplyr)
library(readxl)
library(tidyr)
library(stringr)

xlsx <- "F:/Data/2020W22 Input.xlsx"

ttl <- read_excel(xlsx, sheet = "Total Market") 
comp <- read_excel(xlsx, sheet = "Companies") 
scent <- read_excel(xlsx, sheet = "Scents") 

march_ttl <- ttl$'March Sales'[1]
april_ttl <- march_ttl*(1+ttl$'Growth'[1])


comp['random1'] = comp.apply(lambda x:random.random(),axis=1)
comp['random2'] = comp.apply(lambda x:random.random(),axis=1)
comp['March'] = march_ttl*comp['random1']/comp['random1'].sum()
comp['randomRank'] = comp['random2'].rank().astype(int)
comp['ChangeBps'] = comp['randomRank'].apply(lambda x: -30+x*10)
comp['April'] = april_ttl*(comp['random1']/comp['random1'].sum()+comp['ChangeBps']/10000)


final <- comp %>%
  mutate('random1' = str_extract(`Store`,'(.*)(?=\\s)')) %>%
  pivot_longer(., cols=matches('^(Sales|Profit)'), names_to='Col', values_to='Value') %>%
  separate(`Col`,c('Measure','Date'), sep=' ') %>%
  mutate('Date' = as.Date(`Date`, format='%d/%m/%Y')) %>%
  pivot_wider(., names_from=`Measure`, values_from=`Value`) %>%
  merge(., read_excel(input, 'Staff days worked') %>%
          pivot_longer(., cols=matches('[^(Month)]'), names_to='Store', values_to='Staff days worked'),
        by.x=c('Store','Date'), by.y=c('Store','Month')) %>%
  select(c('Store', 'Category', 'Scent', 'Date', 'Sales', 'Profit', 'Staff days worked'))

View(final)