library(readr)
library(dplyr)
library(tidyr)
library(stringr)

final <- read_csv("C:/Data/PreppinData/Austin_Animal_Center_Outcomes.csv") %>%
  select('Animal Type', 'Outcome Type') %>%
  filter(`Animal Type` %in% c('Cat', 'Dog')) %>%
  mutate('Outcome Type' = if_else(str_detect(`Outcome Type`,'(Adoption|Return to Owner|Transfer)') & !is.na(`Outcome Type`),
                                   'Adopted, Returned to Owner or Transferred','Other')) %>%
  group_by_all() %>%
  summarise('Count' = n(), .groups='drop') %>%
  group_by(`Animal Type`) %>%
  mutate('Ratio' = round(`Count`*100/sum(`Count`),1)) %>%
  pivot_wider(id_cols='Animal Type', names_from = 'Outcome Type', values_from = 'Ratio', values_fn = max)

View(final)
