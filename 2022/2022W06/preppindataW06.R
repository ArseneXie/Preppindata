library(readxl)
library(dplyr)
library(tidyr)
library(splitstackshape)
library(stringr)
library(fuzzyjoin)
options("scipen"=100, "digits"=14)

xlsx <- "C:/Data/PreppinData/7 letter words.xlsx"

scores <- read_excel(xlsx, 'Scrabble Scores') %>%
  separate(`Scrabble`, c('Points', 'TileFreqDtl'), sep='point(s*):', convert=TRUE) %>%
  cSplit(., 'TileFreqDtl', ',', type.convert=FALSE) %>%
  pivot_longer(cols = -'Points', names_to = 'ToDrop', values_to = 'TileFreq', values_drop_na = TRUE) %>%
  mutate('Tile' = str_extract(`TileFreq`,'(\\w+)(?=\\s)'),
         'Frequency' = as.integer(str_extract(`TileFreq`,'(\\d+)$')),
         'LN Chance' = log(`Frequency`/sum(`Frequency`)))

words <- read_excel(xlsx, '7 letter words') %>%  
  mutate('Temp' = toupper(str_replace_all(`7 letter word`,'\\B',','))) %>%
  cSplit(., 'Temp', ',', type.convert=FALSE) %>%
  pivot_longer(cols = -c('7 letter word'), names_to = 'ToDrop', values_to = 'Letter', values_drop_na = TRUE) %>%
  group_by(`7 letter word`, `Letter`) %>%
  mutate('Letter Count' = n()) 

final <- fuzzy_inner_join(words, scores, 
                          by = c('Letter'='Tile','Letter Count'='Frequency'), match_fun = list(`==`, `<=`)) %>%
  group_by(`7 letter word`) %>%
  filter(n()==7) %>%
  summarise('% Chance' = exp(sum(`LN Chance`)),
            '% Chance Temp' = round(`% Chance`,15),
            'Total Points' = sum(`Points`)) %>%
  mutate('Likelihood Rank' = dense_rank(desc(`% Chance Temp`)),
         'Points Rank' = dense_rank(desc(`Total Points`))) %>%
  select(c('Points Rank', 'Likelihood Rank', '7 letter word', '% Chance', 'Total Points'))
  
View(final)