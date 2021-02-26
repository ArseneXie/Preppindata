library(readxl)
library(dplyr)
library(stringr)

df <- read_excel("F:/Data/Shopping List and Ingredients.xlsx", sheet = "Keywords")
keywd <- c(sapply(unlist(strsplit(df[['Animal Ingredients']],',\\s*')), tolower),
           sapply(unlist(strsplit(df[['E Numbers']],',\\s*')),function(x) paste0('e',x)))

shopping <- read_excel("F:/Data/Shopping List and Ingredients.xlsx", sheet = "Shopping List") %>%
  mutate('Check' = strsplit(str_replace_all(tolower(`Ingredients/Allergens`),'\\W+',','),','),
         'Contains' = lapply(`Check`, function(x) paste(sort(intersect(x, keywd)), collapse=', ')))

vegan_list <- shopping %>%
  filter(`Contains`=='') %>%
  select(c('Product', 'Description'))

non_vegan_list <- shopping %>%
  filter(`Contains`!='') %>%
  select(c('Product', 'Description', 'Contains'))

View(vegan_list)
View(non_vegan_list)
