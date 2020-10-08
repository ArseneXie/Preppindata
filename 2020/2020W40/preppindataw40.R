library(dplyr)
library(readxl)
library(tidyr)
library(stringr)
library(splitstackshape)

xlsx <- "F:/Data/Wordsworth Input.xlsx"

final <- read_excel(xlsx, sheet = "Wordsworth Input") %>%
  filter(!str_detect(`DownloadData`,'[<>\\=\\(\\)]') & !str_detect(`DownloadData`,'(Composed|[Ww]ritten) in|^\\s*$')) %>%
  group_by(`Poem`) %>%
  mutate('Line #' = row_number(`RowID`),
         'Line' = str_remove_all(`DownloadData`, '^[^\\w]*'),
         'LineT' = str_remove_all(trimws(toupper(`Line`)),'[^\\w\\s]')) %>%
  cSplit(.,'LineT',' ') %>%
  pivot_longer(.,cols=starts_with('LineT'), names_to='Word #', names_prefix = 'LineT_', values_to='Word' ,values_drop_na=TRUE) %>%
  mutate('WordT' = str_replace_all(`Word`,'\\B',',')) %>%
  cSplit(.,'WordT',',') %>%
  pivot_longer(.,cols=starts_with('WordT'), names_to='ToDrop', values_to='Letter' ,values_drop_na=TRUE) %>%
  merge(.,read_excel(xlsx, sheet = "Scrabble"),by='Letter') %>%
  group_by(`Poem`,`Line #`, `Line`, `Word #`, `Word`) %>%
  summarise('Score' = sum(`Score`)) %>%
  group_by(`Poem`) %>%
  mutate('Highest Scoring Word?' = (`Score`==max(`Score`)))

View(final)
