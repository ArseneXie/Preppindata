library(dplyr)
library(tidyr)
library(readr)
library(purrr)
library(stringr)

fruit_scent = c('Apricot','Lemon','Lime','Pineapple','Raspberry')

final <- dir("E:/", pattern = "MOCK_DATA.*.csv") %>%
  map(~ read_csv(file.path("E:/", .)) 
      %>% mutate('Month' = paste('2019',str_pad(str_extract(.x,'(\\d+)'),2,pad='0'),'01',sep='-'),
                 'Fruit' = ifelse(`Scent` %in% fruit_scent,'Fruit','Non-Fruit'),
                 'All' = 'All')) %>%
  reduce(rbind) %>%
  gather(., key='dummy', value='Type', c('All','Fruit','Month','Product Type'),na.rm=TRUE) %>%
  group_by(`Type`) %>%
  summarise('Total Orders'= n(),
            'Returned Orders'= sum(ifelse(`Return`,1,0)),
            '% Returned' = round(`Returned Orders`/`Total Orders`*100,1))

View(final)