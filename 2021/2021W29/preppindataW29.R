library(readxl)
library(dplyr)
library(tidyr)
library(stringr)
library(stringi)
library(splitstackshape)

Sys.setlocale("LC_ALL","English")

xlsx <- "F:/Data/Olympic Events.xlsx"
final <- read_excel(path = xlsx, sheet = 'Olympics Events') %>%
  mutate('Date' = str_replace_all(`Date`, '(\\d+).+_(\\w+)_(\\d+)', '\\1 \\2 \\3'),
         'UK Date Time' =  as.POSIXct(paste(`Date`, if_else(`Time`=='xx','0:00',`Time`)), '%d %B %Y %H:%M', tz=Sys.timezone()),
         'Date' = as.Date(`Date`, '%d %B %Y'),
         'Venue' = str_to_title(`Venue`),
         'Sport' = stri_replace_all_regex(str_to_title(`Sport`), 
                                          pattern = c('^Artistic Gymnastic.*', '^(Baseball|Softball).*', '^Beach Volley.*',
                                                      '^Boxing.*', '^Rugby.*', '^Skateboarding.*', '^Wrestling.*'), 
                                          replacement = c('Artistic Gymnastic', 'Baseball/Softball', 'Beach Volleyball',
                                                          'Boxing', 'Rugby', 'Skateboarding', 'Wrestling'), 
                                          vectorize_all = FALSE)) %>%
  cSplit(., 'Events', ',') %>%
  pivot_longer(cols=starts_with('Events'), names_to='ToDrop', values_to='Event', values_drop_na = TRUE) %>%
  mutate('Medal Ceremony?' = (str_detect(`Event`, 'Victory Ceremony') | str_detect(`Event`, 'Gold Medal'))) %>%
  merge(., read_excel(path = xlsx, sheet = 'Venues') %>%
          select(c('Venue', 'Location')) %>%
          mutate('Venue' = str_to_title(`Venue`)) %>%
          distinct() %>%
          separate(`Location`, c('Latitude','Longitude'), sep=',', convert=TRUE), by='Venue') %>%
  select(c('UK Date Time', 'Date', 'Sport', 'Event', 'Medal Ceremony?', 'Venue', 'Latitude', 'Longitude'))

View(final)
