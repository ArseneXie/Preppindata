library(readxl)
library(dplyr)
library(xml2)
library(stringr)

xlsx <- "C:/Data/PreppinData/PD Bechdel Test.xlsx"

final <- read_excel(xlsx, 'Webscraping') %>% 
  rowwise() %>%
  mutate('Movie' = str_extract(`DownloadData`, '(?<=>)(([^><])+)(?=<\\/a>)'),
         'Movie' = xml_text(read_html(charToRaw(`Movie`))),
         'Categorisation' = str_extract(`DownloadData`, '(?<=title="\\[)(.*)(?=\\])'),
         'Ranking' = case_when(
           `Categorisation`=='There are two or more women in this movie and they talk to each other about something other than a man' ~ 1,
           `Categorisation`=='There are two or more women in this movie and they talk to each other about something other than a man, although dubious' ~ 2,
           `Categorisation`=='There are two or more women in this movie, but they only talk to each other about a man' ~ 3,
           `Categorisation`=="There are two or more women in this movie, but they don't talk to each other" ~ 4,
           TRUE ~ 5),
         'Pass/Fail' = if_else(`Ranking`<=2, 'Pass', 'Fail')) %>%
  group_by(`Movie`, `Year`) %>%
  filter(`Ranking` == max(`Ranking`)) %>%
  select(c('Movie', 'Year', 'Pass/Fail', 'Ranking', 'Categorisation')) %>%
  distinct()

View(final)
