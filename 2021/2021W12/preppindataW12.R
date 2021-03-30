library(readr)
library(dplyr)
library(tidyr)
library(stringr)

Sys.setlocale("LC_ALL","English")

trans_date <- function (x){
  d <- as.Date(paste0('01-',x), format='%d-%b-%y')
  return(d)
}

final <- read_csv("F:/Data/Tourism Input.csv", col_types = cols(.default = "c")) %>%
  filter(`Unit-Detail`=='Tourists' & `Series-Measure`!='Total tourist arrivals') %>%
  pivot_longer(matches('\\w{3}-\\d{2}') , names_to = 'Month', values_to='Original Tourists',
               names_transform = list(`Month` = trans_date),
               values_transform = list(`Original Tourists`= as.integer), values_drop_na = TRUE) %>%
  mutate('CountryLevel' = str_detect(`Hierarchy-Breakdown`,'(.*/){3}\\s(.*)'),
         'Breakdown' = if_else(`CountryLevel`,
                               str_extract(`Hierarchy-Breakdown`,'(?<=/\\s)([^/]*)$'),
                               str_extract(`Series-Measure`,'(?<=(from|-)\\s)(.*)')),
         'Country' = if_else(`CountryLevel`,str_replace(`Series-Measure`,'.*from\\s(?:the\\s)*',''),'Unknown')) %>%
  group_by(`Month`,`Breakdown`) %>%
  mutate('Number of Tourists' = `Original Tourists` + 
           if_else(`CountryLevel`, 0, sum(if_else(`CountryLevel`,-1*`Original Tourists`,0)))) %>%
  select(c('Month', 'Breakdown', 'Country', 'Number of Tourists'))

View(final)
