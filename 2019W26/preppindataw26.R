library(readxl)
library(dplyr)
library(tidyr)
library(splitstackshape)


final <- read_excel('E:/PD - Wk 26 Cocktails.xlsx') %>%
  rename('Cocktails' = !!names(.[1]),
         'Ingredient' = !!names(.[2]),
         'Cocktail Price' = !!names(.[3])) %>%
  cSplit(., 'Ingredient', ',') %>%
  gather(., key='Ingredient Position', value='Ingredient Split', starts_with('Ingredient_'),na.rm=TRUE) %>%
  mutate('Ingredient Position' = as.integer(gsub('[^0-9]','',`Ingredient Position`))) %>%
  group_by(`Ingredient Split`) %>%
  mutate('Average Ingredient Price' = mean(`Cocktail Price`))

View(final)