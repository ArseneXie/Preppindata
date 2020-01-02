library(readxl)
library(readr)
library(dplyr)
library(tidyr)
library(splitstackshape)

final <- read_excel("E:/Wow _ PD data set.xlsx", 
                            sheet = "Gigs Data", col_types = c("numeric", 
                                                               "text", "date", "text", "text", "text")) %>%
  select(-'ConcertID') %>%
  {. ->> gigs} %>%
  .[!duplicated( gigs %>% mutate_all(., .funs=toupper)),] %>%
  mutate('All Artists' = if_else(grepl('\\/',`Concert`), `Concert`, `Artist`)) %>%
  cSplit(., 'All Artists', '/') %>% 
  gather(., key='var', value='Fellow Artist', starts_with('All Artists'),na.rm=TRUE) %>%
  select(-('var')) %>%
  mutate('Fellow Artist' = if_else(`Fellow Artist`==`Artist`, '', `Fellow Artist`)) %>%
  merge(.,home <- read_excel("E:/Wow _ PD data set.xlsx", 
                             sheet = "Home Locations") %>%
          rename('Home Longitude' = 'Longitude') %>%
          rename('Home Latitude' = 'Latitude'), by='Artist') %>%
  merge(.,loc <- read_csv("E:/LongLats.csv") %>%
          separate(`LongLats`, c('Longitude', 'Latitude'), sep = ',', convert= TRUE)
        , by='Location', all.x=TRUE)

View(final)