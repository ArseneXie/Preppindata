library(readxl)
library(dplyr)
library(tidyr)

xls = "E:/PD Wk 44 Input.xlsx"

final <- read_excel(path = xls, sheet = 'Store Sales') %>%
  gather(., key='Store', value='Store Sales', -'Date',na.rm=TRUE) %>%
  merge(.,read_excel(path = xls, sheet = 'Team Member Days'), on=c('Store','Date')) %>%
  group_by(`Store`,`Date`) %>%
  mutate('Daily Avg Sales' = `Store Sales`/n()) %>%
  group_by(`Store`,`Team Member`) %>%
  summarise('Estimated Sales From Staff Member' = format(mean(`Daily Avg Sales`),nsmall=2)) %>%
  group_by(`Store`) %>%
  mutate('Rank' = rank(desc(as.numeric(`Estimated Sales From Staff Member`))))
  
View(final)  