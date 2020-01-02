library(readxl)
library(dplyr)
library(tidyr)

common_words <- read_excel("H:/PD - Week 9 Complaints.xlsx", 
                           sheet = "Common English Words")
complaints <- read_excel("H:/PD - Week 9 Complaints.xlsx", 
                         sheet = "Complaints")

df <- complaints %>%
  mutate("Tweet" = gsub('@C&BSudsCo','',`Tweet`)) %>%
  mutate("Tweet" = trimws(gsub('[[:punct:]]+','',`Tweet`))) 

max_word <- as.numeric(unlist(lapply(df, function(x) max(sapply(strsplit(x, " "), length)))))

dt <- df %>%
  separate(`Tweet`, paste0("dummy_", seq(1:max_word)))

final <- merge(df, dt, by.x = 0, by.y = 0) %>%
  select(-("Row.names")) %>%
  gather(., key="var", value="Word", -`Tweet`) %>%
  select(-("var")) %>%
  drop_na() %>%
  mutate("Key" = tolower(`Word`)) %>%
  anti_join(., common_words %>% mutate("Key" = tolower(`Word`)), by="Key") %>%
  select(c("Word","Tweet"))

View(final)