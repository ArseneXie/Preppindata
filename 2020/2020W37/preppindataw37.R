library(dplyr)
library(readxl)
library(tidyr)
library(splitstackshape)
library(fuzzyjoin)

xlsx <- "F:/Data/School Timetables-4.xlsx"

supply <- read_excel(xlsx, sheet = 'Teachers') %>%
  separate(`Ages Taught`, c('fromAge','toAge'),sep='-') %>%
  cSplit(., 'Working Days', ',',type.convert = FALSE) %>%
  pivot_longer(.,cols=starts_with('Working Days'),names_to = 'ToDrop', values_to = 'Working Days', values_drop_na = TRUE) %>%
  group_by(`Name`,`Working Days`) %>%
  mutate('Allocated Hours' = 6/n()) %>%
  group_by(`Subject`) %>%
  mutate('Potential Teachers Hours' = sum(`Allocated Hours`)) %>%
  select(-c('ToDrop','Working Days','Allocated Hours')) %>%
  distinct() %>%
  rename('Subjects' = 'Subject')

final <- read_excel(xlsx, sheet = 'Students') %>%
  cSplit(., 'Subject', '/') %>%
  pivot_longer(.,cols=starts_with('Subject'),names_to = 'ToDrop', values_to = 'Subject', values_drop_na = TRUE) %>%
  fuzzy_inner_join(.,read_excel(xlsx, sheet = 'Hours') %>% separate(`Age Group`, c('fromAge','toAge'),sep='-'),
                   by = c('Age'='fromAge','Age'='toAge'),
                   match_fun = list(`>=`, `<=`)) %>%
  select(-c('ToDrop','fromAge','toAge')) %>%
  group_by(`Subject`,`Age`) %>%
  summarise('Students Count' = n(),
            'Hours teaching per week' = first(`Hours teaching per week`)) %>%
  fuzzy_inner_join(.,supply,
                   by = c('Subject'='Subjects','Age'='fromAge','Age'='toAge'),
                   match_fun = list(`==`,`>=`, `<=`)) %>%
  merge(.,read_excel(xlsx, sheet = 'Rooms') %>% group_by(`Subjects`) %>% summarise('Capacity'=sum(`Capacity`)),by='Subjects') %>%
  mutate('Classes required' = ceiling(`Students Count`/`Capacity`),
         'Teaching Hours needed' = `Classes required`*`Hours teaching per week`) %>%
  group_by(`Subject`) %>%
  summarise('Potential Teachers Hours' = first(`Potential Teachers Hours`),
            'Total Teaching Hours needed' = sum(`Teaching Hours needed`),
            'Classes required' = sum(`Classes required`),
            '% utilised' = round(`Total Teaching Hours needed`/`Potential Teachers Hours`*100))

View(final)
