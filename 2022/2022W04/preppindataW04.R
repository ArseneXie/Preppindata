library(dplyr)
library(tidyr)
library(readr)
library(stringi)

final <- read_csv("C:/Data/PreppinData/PD 2021 WK 1 to 4 ideas - Preferences of Travel.csv") %>%
  pivot_longer(col=-'Student ID', names_to='Weekday', values_to = 'Method of Travel') %>%
  mutate('Method of Travel' = stri_replace_all_regex(`Method of Travel`, pattern = c('^B.*', '^Ca.*', '^Hel.*', '^Sco.*', '^W.*'),
                                                     replacement = c('Bicycle', 'Car', 'Helicopter', 'Scooter', 'Walk'), 
                                                     vectorize_all = FALSE)) %>%
  group_by(`Weekday`) %>%
  mutate('Trips per Day' = n()) %>%
  group_by(`Weekday`, `Method of Travel`, `Trips per Day`) %>%
  summarise('Number of Trips' = n(), .groups = 'drop') %>%
  mutate('Sustainable?' = if_else(`Method of Travel` %in% c('Car', 'Van', 'Aeroplane', 'Helicopter'), 'Non-Sustainable', 'Sustainable'),
         '% of trips per day' = round(`Number of Trips`/`Trips per Day`, 2)) %>%
  arrange(`Weekday`, `Sustainable?`) %>%
  select(c('Sustainable?', 'Method of Travel', 'Weekday', 'Number of Trips', 'Trips per Day', '% of trips per day'))

View(final)
