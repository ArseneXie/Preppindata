library(readxl)
library(dplyr)
library(lubridate)

today <- as.POSIXct('2022-04-13', tz ='UTC')

final <- read_excel("C:/Data/PreppinData/Rental Contracts.xlsx") %>% 
  mutate('Contract Length' = round(time_length(floor_date(`Contract End`,'month') - floor_date(`Contract Start`,'month'), 'month')),
         'Months Until Expiry' =  round(time_length(floor_date(`Contract End`,'month') - floor_date(today,'month'), 'month'))) %>%
  merge(read_excel("C:/Data/PreppinData/Office Space Prices.xlsx"), by=c('City', 'Office Size')) %>%
  .[rep(seq_len(nrow(.)), .[['Contract Length']]),] %>%
  group_by(`ID`) %>%
  mutate('Seq' = row_number(`ID`),
         'Month Divider' = `Contract Start` %m+% months(`Seq`-1),
         'Cumulative Monthly Cost' = `Rent per Month`*`Seq`) 
  
output1 <- final %>%
  select(c('Cumulative Monthly Cost', 'ID', 'Country', 'City', 'Address', 'Company', 'Office Size',
           'Contract Start', 'Contract End', 'Contract Length', 'Months Until Expiry', 'People', 'Per Person', 
           'Rent per Month', 'Month Divider'))
  
output2 <- final %>%
  mutate('Year' = year(`Month Divider`),
         'Paid Rent' = if_else(floor_date(`Month Divider`,'month')<=floor_date(today,'month'), `Rent per Month`, 
                               if_else(year(`Month Divider`)<=year(today), 0, NA_real_))) %>%
  group_by(`Year`) %>%
  summarise('EoY and Current' = sum(`Paid Rent`))
  
View(output1)
View(output2)
