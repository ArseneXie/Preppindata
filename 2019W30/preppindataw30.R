library(readxl)
library(dplyr)
library(tidyr)
library(splitstackshape)
library(stringr)

final <- read_excel("E:/@serpsswimclub_user_tweets.xlsx", 
                    sheet = "tweets") %>%
  select(c('Tweet Id','Text', 'Created At')) %>%
  mutate('Water-TempF' = str_extract(`Text`,'(?<=Water\\s-\\s)-*\\d+\\.*\\d*'),
         'Water-TempC' = str_extract(`Text`,'-*\\d+\\.*\\d*(?=C;)'),
         'Air-TempF' = str_extract(`Text`,'(?<=Air\\s-\\s)-*\\d+\\.*\\d*'),
         'Air-TempC' = str_extract(`Text`,'-*\\d+\\.*\\d*(?=C\\.)'),
         'Comment' = str_extract(`Text`,'(?<=C\\.).*'),
         'CommentTemp' = tolower(trimws(str_replace_all(`Comment`,'[[:punct:]]+','')))) %>%
  drop_na() %>%
  cSplit(., 'CommentTemp', ' ') %>%
  gather(., key='var', value='Comment Split', starts_with('CommentTemp'),na.rm=TRUE) %>%
  select(-c('var','Text')) %>%
  anti_join(., common_words <- read_excel("E:/Common English Words.xlsx",
                                          sheet = "Sheet1") %>%
              mutate('Key' = tolower(`Word`)), by=c('Comment Split'='Key')) %>%
  gather(., key='CateTemp', value='R2CVal', contains('-Temp'),na.rm=TRUE) %>%
  mutate_at(vars('R2CVal'),as.numeric) %>%
  separate(`CateTemp`,c('Category','R2CCol')) %>%
  distinct() %>%
  spread(`R2CCol`,`R2CVal`)
              
View(final)


final2 <- final %>%
  filter(str_detect(`Comment Split`,'^[a-z]')) 
nrow(final2)

