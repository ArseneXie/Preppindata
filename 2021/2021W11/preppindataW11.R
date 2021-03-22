library(readxl)
library(dplyr)
library(tidyr)
library(splitstackshape)
library(stringr)

xlsx <- "F:/Data/Cocktails Dataset.xlsx"

final <- read_excel(xlsx, sheet = "Cocktails") %>%
  cSplit(., 'Recipe (ml)', ';') %>%
  pivot_longer(starts_with('Recipe'), names_to = 'ToDrop', values_to='Recipe', values_drop_na=TRUE) %>%
  separate(`Recipe`, c('Ingredient','Measurement'), sep=':' ) %>%
  merge(read_excel(xlsx, sheet = "Sourcing") %>%
          merge(read_excel(xlsx, sheet = "Conversion Rates"), by='Currency'), by='Ingredient') %>%
  group_by(`Cocktail`) %>%
  summarise('Cost' = round(sum(as.numeric(str_extract(`Measurement`,'(\\d+)'))*`Price`
                               /`ml per Bottle`/`Conversion Rate ¢G`),2),
            'Price' = max(`Price (¢G)`),
            'Margin' = `Price` - `Cost`, .groups='drop') %>%
  select(c('Cocktail', 'Price', 'Cost', 'Margin'))

View(final)
