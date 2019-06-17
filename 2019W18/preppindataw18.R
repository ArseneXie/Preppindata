library(readxl)
library(dplyr)
library(tidyr)

anime <- read_excel("E:/anime.xlsx", sheet = "anime", 
                    col_types = c("text", "text", "text", 
                                  "text", "text", "numeric", "numeric")) %>%
  filter((`type`=='Movie' | `type`=='TV') & `members`>=10000) %>%
  drop_na() 

max_genre <- as.numeric(unlist(lapply(anime %>% select('genre'), function(x) max(sapply(strsplit(x, ','), length)))))

final <-  anime  %>%
  separate(`genre`, paste0("genre_split_", seq(1:max_genre)), sep = ',') %>%
  select(-c('anime_id','episodes')) %>%
  gather(., key="var", value="Genre", -c('name','type','rating','members')) %>%
  mutate('Genre' = trimws(`Genre`)) %>%
  select(-("var")) %>%
  drop_na() %>%
  group_by(`Genre`,`type`) %>%
  mutate('Avg Rating' = mean(`rating`),
         'Avg Viewers' = mean(`members`),
         'Max Rating' = max(`rating`)) %>%
  filter(`rating`==`Max Rating`) %>%
  rename('Type' = 'type',
         'Prime Example' = 'name') %>%
  select(c('Genre','Type','Avg Rating','Max Rating','Avg Viewers','Prime Example'))

View(final)