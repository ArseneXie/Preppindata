library(dplyr)
library(readxl)
library(tidyr)
library(stringr)

xlsx <- "F:/Data/Medals PD WOW.xlsx"

country_code_map <- read_excel(xlsx, sheet = 'Country Codes') 

finalA <- read_excel(xlsx, sheet = 'Medallists', col_types = c("text", 
                                                               "text", "text", "text", "text", "text", 
                                                               "text", "text", "text")) %>%
  merge(country_code_map, by = 'Country', all.x = TRUE) %>%
  mutate('Code' = if_else(is.na(`Code`),`Country Code`,`Code`)) %>%
  rename('CountryDrop' = 'Country') %>%
  merge(country_code_map, by = 'Code') %>%
  mutate('Event' = str_replace_all(`Event`,'(?<!kilo)(metre(s*))','m'),
         'Event' = str_replace_all(`Event`,'(kilometre(s*))','km'),
         'Sport' = str_replace_all(`Sport`,'^Canoe.*','Canoeing'),
         'Sport' = str_replace_all(`Sport`,'^Swimming$','Aquatics'),
         'Discipline' = str_replace_all(`Discipline`,'Beach volley.*','Beach Volleyball'),
         'Discipline' = str_replace_all(`Discipline`,'Wrestling.*','Wrestling'),
         'Discipline' = str_replace_all(`Discipline`,'Rhythmic.*','Rhythmic'),
         'Discipline' = str_replace_all(`Discipline`,'Artistic.*','Artistic'),
         'Discipline' = str_replace_all(`Discipline`,'Mountain (B|b)ik.*','Mountain Bike'),
         'Discipline' = str_replace_all(`Discipline`,'Modern (P|p)en.*','Modern Pentath.'),
         'Discipline' = str_replace_all(`Discipline`,'(.*) cycling','Cycling \\1')) %>%
  select(c('Country', 'Code', 'Sport', 'Medal', 'Event', 'Athlete', 'Year', 'Event_Gender', 'Discipline'))

finalB <- finalA %>% 
  group_by(`Country`, `Year`, `Medal`) %>%
  summarise('Value' = n()) %>%
  pivot_wider(., names_from = `Medal`, values_from = `Value`, values_fn = list(Value=sum)) %>%
  select(c('Country', 'Year', 'Gold', 'Silver', 'Bronze'))

finalC <- read_excel(xlsx, sheet = 'Hosts',col_types = c("text", 
                                                         "text", "text", "text", "numeric", 
                                                         "numeric", "numeric")) %>%
  separate(., `Host`, c('Host City', 'Host Country'), sep = ',\\s') %>%
  mutate('Start Date' = if_else(str_detect(`Start Date`,'/'),
                                as.Date(`Start Date`,format='%m/%d/%Y'),
                                as.Date(as.numeric(`Start Date`), origin = '1899-12-30')),
         'End Date' = if_else(str_detect(`End Date`,'/'),
                                as.Date(`End Date`,format='%m/%d/%Y'),
                                as.Date(as.numeric(`End Date`), origin = '1899-12-30')),
         'Year' = as.integer(strftime(`Start Date`,format = '%Y'))) %>%
  select(c('Year', 'Host Country', 'Host City', 'Start Date', 'End Date', 'Games', 'Nations', 'Sports', 'Events'))

View(finalA)
View(finalB)
View(finalC)