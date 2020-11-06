library(dplyr)
library(tidyr)
library(readxl)
library(lubridate)
library(stringr)
library(stringi)

final <- read_excel("F:/Data/Halloween Costumes.xlsx") %>%
  mutate('Date' = as.Date(`Date`,"%d/%m/%Y"),
         'fiscalYear' = as.integer(quarter(`Date`,with_year = TRUE, fiscal_start = 11))) %>%
  filter(`fiscalYear`>=2019) %>%
  mutate('Costume' = stri_replace_all_regex(`Costume`,
                                            pattern = c("^[CKG].*at.*", "^[CK]l.*n$", "^D.*(ev|ia).*", "^Dino.*", "^G.*t$",
                                                        "^Pira.*", "^Vamp.*", "^We.*wolf$", "^Z.*mbi.*"),
                                            replacement = c("Cat", "Clown", "Devil", "Dinosaur", "Ghost",
                                                            "Pirate", "Vampire", "Werewolf", "Zombie"), vectorize_all = FALSE),
         'Country' = stri_replace_all_fixed(`Country`, 
                                            pattern = c("Indonsia", "Slovnia", "Philippins", "Luxmbourg"),
                                            replacement = c("Indonesia", "Slovenia", "Philippines", "Luxembourg"), vectorize_all = FALSE),
         'fiscalYear' = paste(fiscalYear, 'EY Sales')) %>%
  pivot_longer(.,cols=starts_with('Sales'), names_to='Price', names_pattern='(?<=at\\s)(\\w+)(?=\\s)', values_to='Draft Sales' ,values_drop_na=TRUE) %>%
  mutate('Currency' = str_extract(`Draft Sales`,'(.*)(?=\\s+\\d)'),
         'Sales' = as.integer(str_extract_all(`Draft Sales`,'(\\d+\\.\\d+$)'))) %>%
  select(-c('Date','Draft Sales')) %>%
  pivot_wider(., names_from='fiscalYear', values_from='Sales', values_fn = sum)
  
View(final)