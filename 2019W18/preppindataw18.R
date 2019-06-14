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
  mutate('Genre' = )
  select(-("var")) %>%
  drop_na() 


test <- final %>%
  filter(`genre`==' Shounen')
  
test2 <- anime  %>%
  separate(`genre`, paste0("genre_split_", seq(1:max_genre)), sep = ',') %>%
  select(-c('anime_id','episodes')) %>%
  gather(., key="var", value="Genre", -c('name','type','rating','members')) %>%
  filter(`Genre`==' Shounen')

%>%
  group_by(`Genre`,`type`) %>%
  mutate('Prime Example' = which.max(table(`rating`))) 



final <- merge(df, dt, by.x = 0, by.y = 0) %>%
  select(-("Row.names")) %>%
  gather(., key="var", value="Word", -`Tweet`) %>%
  select(-("var")) %>%
  drop_na() %>%
  mutate("Key" = tolower(`Word`)) %>%
  anti_join(., common_words %>% mutate("Key" = tolower(`Word`)), by="Key") %>%
  select(c("Word","Tweet"))

View(final)