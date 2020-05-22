library(dplyr)
library(readr)
library(tidyr)
library(scales)

df <- read_csv("F:/Data/2020W21 Input.csv") %>%
  mutate('Group' = if_else(`Company`=='Chin & Beard Suds Co','C&BSCo','Rest of Market'))

finalA <- df %>% group_by(`Company`,`Month`) %>%
  mutate('CM Total' = sum(`Sales`)) %>%
  group_by(`Month`) %>%
  mutate('Mon Total' = sum(`Sales`)) %>%
  pivot_longer(.,cols=matches('Total$'), names_to='Measure', values_to='R2CVal') %>%
  unite('R2CCol','Month','Measure',sep=' ') %>%
  pivot_wider(.,id_cols='Company', names_from='R2CCol', values_from='R2CVal',values_fn = list(R2CVal = max)) %>%
  mutate('Growth' = label_percent(0.01)((`April CM Total`-`March CM Total`)/`March CM Total`),
         'April Market Share' = round(`April CM Total`/`April Mon Total`*100,2),
         'Bps Change' = round((`April CM Total`/`April Mon Total`-`March CM Total`/`March Mon Total`)/0.0001)) %>%
  select(c('Company', 'Growth','April Market Share', 'Bps Change'))


finalB <- df %>% group_by(`Soap Scent`,`Group`,`Month`) %>%
  mutate('SGM Total' = sum(`Sales`)) %>%
  group_by(`Group`,`Month`) %>%
  mutate('GM Total' = sum(`Sales`)) %>%
  pivot_longer(.,cols=matches('Total$'), names_to='Measure', values_to='R2CVal') %>%
  unite('R2CCol','Month','Measure',sep=' ') %>%
  pivot_wider(.,id_cols=c('Soap Scent','Group'), names_from='R2CCol', values_from='R2CVal',values_fn = list(R2CVal = max)) %>%
  mutate('R2CCol' = paste(`Group`,'Contribution to Growth'),
         'R2CVal' = round((`April SGM Total`-`March SGM Total`)/`March GM Total`*100,2)) %>%
  pivot_wider(.,id_cols=c('Soap Scent'), names_from='R2CCol', values_from='R2CVal',values_fn = list(R2CVal = max)) %>%
  mutate('Outperformance' = `C&BSCo Contribution to Growth`-`Rest of Market Contribution to Growth`) %>%
  select(c('Soap Scent','C&BSCo Contribution to Growth','Rest of Market Contribution to Growth','Outperformance'))

View(finalA)
View(finalB)