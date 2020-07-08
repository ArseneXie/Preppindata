library(dplyr)
library(readxl)
library(tidyr)
library(stringr)
library(splitstackshape)

xlsx <- "F:/Data/Input.xlsx"
rel_val <- c('Rarely Breaks', 'Inconsistent', 'Fairly Inconsistent', 'Fairly Consistent', 'Very Consistent')

final <- read_excel(xlsx, sheet = 'Preppers') %>%
  cSplit(., 'Season', ',') %>%
  pivot_longer(., cols=starts_with('Season'), names_to='To Drop', values_to  = 'Season Split', values_drop_na = TRUE) %>%
  select(-'To Drop') %>%
  cSplit(., 'Board Type', ',') %>%
  pivot_longer(., cols=starts_with('Board Type'), names_to='To Drop', values_to  = 'Boards Split', values_drop_na = TRUE) %>%
  select(-'To Drop') %>%
  merge(read_excel(xlsx, sheet = 'Location'),all = TRUE) %>%
  rowwise() %>%
  filter(`Season Split` %in% str_trim(str_split(`Surf Season`,',')[[1]])) %>%
  separate(`Site`,c('Surf Site','To Drop'), sep='\\s-') %>%
  merge(read_excel(xlsx, sheet = 'Information', skip=1) %>% drop_na(), by='Surf Site') %>%
  rowwise() %>%
  filter((`Boards Split` %in% str_trim(str_split(`Boards`,',')[[1]])) & (`Skill` %in% str_trim(str_split(`Skill Level`,',')[[1]]))) %>%
  ungroup() %>%
  select(c('Name', 'Surf Site', 'Swell Direction', 'Reliability', 'Wind Direction', 'Type', 'Boards', 'Skill Level', 'Surf Season','Rating')) %>%
  distinct() %>%
  mutate('RatingRel'= `Rating`+match(`Reliability`,rel_val)/100) %>%
  group_by(`Name`) %>%
  filter(`RatingRel` == max(`RatingRel`)) %>%
  select(-'RatingRel')

View(final)