library(readxl)
library(dplyr)
library(tidyr)
library(stringr)

final <- read_excel("F:/Data/Preppin Data Challenge.xlsx") %>%
  mutate_at(ncol(.),  as.numeric) %>%
  drop_na(`Name, Age, Area of Work`) %>%
  select(-'Project') %>%
  pivot_longer(cols=-'Name, Age, Area of Work', names_to='DateInNum', values_to='Hours', values_drop_na=TRUE) %>%
  mutate('Name' = str_extract(`Name, Age, Area of Work`,'^([^,]*)'),
         'Area of Work' = str_extract(`Name, Age, Area of Work`,'(?<=:\\s)(.*)$'))%>%
  group_by(`Name`) %>%
  mutate('Avg Number of Hours worked per day' = sum(`Hours`)/n_distinct(`DateInNum`),
         '% of Total' = sum(if_else(`Area of Work`=='Client',`Hours`,0))/sum(if_else(`Area of Work`=='Chats',0,`Hours`)),
         '% of Total' = paste0(round(`% of Total`*100),'%')) %>%
  filter(`Area of Work` == 'Client') %>%
  select(c('Name', 'Area of Work', '% of Total', 'Avg Number of Hours worked per day')) %>%
  distinct()

View(final)
