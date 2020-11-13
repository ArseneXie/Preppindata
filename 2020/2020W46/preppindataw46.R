library(dplyr)
library(readxl)
library(stringr)
library(fuzzyjoin)

Sys.setlocale("LC_ALL","English")
xlsx <- "F:/Data/Incident List.xlsx"
finalA <- read_excel(xlsx, sheet = "Incident List") %>%
  mutate('Date' = as.Date(str_replace_all(`Incident`,'.*([A-Z][a-z]{2})\\s(\\d+)[a-z]{2}\\s(\\d{4}).*','\\2-\\1-\\3'),'%d-%b-%Y'),
         'Location' = if_else(str_detect(`Incident`, '(\\sat\\s.*\\son\\s)'),
                              str_extract(`Incident`,'(?<=at\\s)(.*?)(?=\\son\\s)'), str_extract(`Incident`, '(?<=near\\s)(.*?)(?=\\son\\s)')),
         'Aircraft' = str_extract(`Incident`,'(.*?)(?=\\s(at|near)\\s)'),
         'Incident Description' = str_extract(`Incident`,'(?<=\\d{4},\\s)(.*$)')) %>%
  select(-c('RecordID', 'Incident'))

finalB <- finalA %>% select('Incident Description') %>%
  regex_inner_join(read_excel(xlsx, sheet = "Category") %>% 
                     mutate('Key' = paste0('.*',str_sub(tolower(`Category`),1,5),'.*')), by = c(`Incident Description`='Key')) %>%
  group_by(`Category`) %>%
  summarise('Number of Incidents' = n(), .groups = 'drop')
   
View(finalA)
View(finalB)
