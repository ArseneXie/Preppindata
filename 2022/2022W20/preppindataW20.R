library(readxl)
library(dplyr)
library(stringi)
library(stringr)

xlsx <- "C:/Data/PreppinData/TC22 Input.xlsx"

final <-  read_excel(xlsx, 'Registrations') %>%
  group_by(`Email`) %>%
  mutate('Online/In Person' = stri_replace_all_regex(`Online/In Person`, pattern = c('^O.*', '^I.*'), 
                                                     replacement = c('Online', 'In Person'), vectorize_all = FALSE),
         'Company' = str_extract_all(`Email`, '(?<=@)([^\\.]+)'),
         'Planning to attend' = n_distinct(`Session ID`)) %>%
  merge(read_excel(xlsx, 'Sessions'), by='Session ID') %>%
  anti_join(read_excel(xlsx, 'In Person Attendees'), by = c('Session', 'First Name', 'Last Name')) %>%
  anti_join(read_excel(xlsx, 'Online Attendees'), by = c('Session', 'Email')) %>%
  group_by(`Email`) %>%
  mutate('Not Attended %' = n_distinct(`Session ID`)/`Planning to attend`*100) %>%
  rename('Session not attended' = 'Session') %>%
  select(c('Company', 'First Name', 'Last Name', 'Email', 'Online/In Person', 'Session not attended', 'Not Attended %'))
  
View(final)
