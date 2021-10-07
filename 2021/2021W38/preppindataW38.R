library(readxl)
library(dplyr)
library(tidyr)

input <- "C:/Data/PreppinData/Trilogies Input.xlsx"

final <- read_excel(path = input, sheet = 'Films') %>%
  separate(`Number in Series`, c('Film Order', 'Total Films in Series'), convert=TRUE) %>%
  group_by(`Trilogy Grouping`) %>%
  mutate('Trilogy Average' = mean(`Rating`),
         'Trilogy Highest' = max(`Rating`)) %>%
  ungroup() %>%
  mutate('Trilogy Ranking' = dense_rank(interaction(desc(`Trilogy Average`), desc(`Trilogy Highest`), lex.order=T))) %>%
  merge(read_excel(path = input, sheet = 'Top 30 Trilogies'), by='Trilogy Ranking') %>%
  mutate('Trilogy' = gsub('\\s+trilogy$', '', `Trilogy`),
         'Trilogy Average' = round(`Trilogy Average`, 1)) %>%
  select(c('Trilogy Ranking','Trilogy','Trilogy Average','Film Order','Title','Rating','Total Films in Series'))

View(final)
