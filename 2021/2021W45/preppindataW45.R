library(readxl)
library(dplyr)
library(tidyr)
library(purrr)
library(stringr)
library(splitstackshape)
library(fuzzyjoin)

Sys.setlocale("LC_ALL","English")
input <- "C:/Data/PreppinData/TC Input.xlsx"

meeting <- input %>%
  excel_sheets() %>% .[grepl('.*Nov$',.)] %>%
  set_names() %>%
  map_df(
    ~ read_excel(path = input, sheet = .x, col_types = c("numeric", "date", "text", "text")),
    .id = 'Date') %>%
  mutate('Date' = paste(str_remove(`Date`,'th'),2021),
         'Time' = if_else(as.integer(format(`Session Time`,'%Y'))>=1900, paste0(as.character(format(`Session Time`, "%d")),':00'), 
                          as.character(format(`Session Time`, "%H:%M"))),
         'DateTime' = as.POSIXct(paste(`Date`,`Time`), format="%d %b %Y %H:%M")) %>%
  select(c('Session ID', 'DateTime', 'Subject','Attendee IDs')) %>%
  cSplit(., 'Attendee IDs', ',') %>%
  pivot_longer(., cols=starts_with('Attendee'), names_to='ToDrop', values_to = 'Attendee ID', values_drop_na=TRUE) %>%
  merge(., read_excel(input, 'Attendees'), by='Attendee ID') %>%
  select(c('Session ID', 'DateTime', 'Subject', 'Attendee'))

direct <- meeting %>%
  merge(., meeting %>% select(c('Session ID', 'Attendee')) %>% rename('Contact'='Attendee'), by='Session ID') %>%
  filter(`Attendee` != `Contact`) %>%
  select(-'Session ID') 

indirect <- direct %>% rename('Direct'='Contact') %>%
  fuzzy_inner_join(.,direct %>% rename('Direct'='Attendee'),
                   by=c('DateTime', 'Subject', 'Direct'),
                   match_fun = list(`>`,`==`,`==`)) %>%
  rename('Subject' = 'Subject.x') %>%
  filter(`Attendee` != `Contact`) 

final <- rbind(direct %>% mutate('Contact Type'='Direct Contact') %>% select(c('Subject', 'Attendee', 'Contact Type', 'Contact')),
               indirect %>% mutate('Contact Type'='Indirect Contact') %>% select(c('Subject', 'Attendee', 'Contact Type', 'Contact'))) %>%
  arrange(`Attendee`, `Subject`, `Contact`, `Contact Type`) %>%
  group_by(`Subject`, `Attendee`, `Contact`) %>%
  mutate('Type Index' = row_number(`Contact Type`)) %>%
  filter(`Type Index`==1) %>%
  select(-'Type Index')
    
View(final)
