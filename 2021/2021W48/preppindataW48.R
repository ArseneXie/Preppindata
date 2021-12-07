library(readxl)
library(dplyr)
library(tidyr)
library(stringr)

final <- read_excel("C:/Data/PreppinData/PD 2021 Wk 48 Input.xlsx", col_names = FALSE) %>%
  drop_na() %>%
  `colnames<-`(c('Measure','Val1','Val2')) %>%
  mutate('Branch' = if_else(str_detect(`Val1`,'([A-z])'),`Measure`, NA_character_)) %>%
  fill(`Branch`, .direction = "down") %>%
  `colnames<-`(c('Measure', .[[1,2]], .[[1,3]], 'Branch')) %>%
  filter(`Branch`!=`Measure`) %>%
  pivot_longer(cols=-c('Measure','Branch'), names_to='Recorded Year', names_pattern='\\D+(\\d+)', values_to='Value') %>%
  mutate('Clean Measure Names' = str_remove(`Measure`,'(\\s\\(.\\))$'),
         'Factor' = paste0(str_extract(`Measure`,'(?<=\\()(.)(?=\\)$)'),''),
         'True Values' = if_else(`Factor`=='m',1000000,if_else(`Factor`=='k',1000,1))*as.numeric(`Value`)) %>%
  select(c('Branch', 'Clean Measure Names', 'Recorded Year', 'True Values'))
  
View(final)
