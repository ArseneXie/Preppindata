library(dplyr)
library(readxl)

final <- read_excel("F:/Data/Input - Anagrams.xlsx", sheet = "Anagrams") %>%
  rowwise() %>%
  mutate('Anagram?'= (paste(sort(unlist(strsplit(tolower(`Word 1`), ''))), collapse = '')==
                        paste(sort(unlist(strsplit(tolower(`Word 2`), ''))), collapse = '')))

View(final)
