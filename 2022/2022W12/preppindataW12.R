library(dplyr)
library(readr)
library(purrr)
library(stringr)

filepath <- "C:/Data/PreppinData/UK Gender Pay Gap Data/"

final <- dir(filepath) %>%
  map(~ read_csv(file.path(filepath, .)) %>% 
        select(c('EmployerName', 'EmployerId', 'EmployerSize', 'DiffMedianHourlyPercent')) %>%
        mutate('Year' = str_extract(.x,'(\\d+)'),
               'Report' = str_extract(.x,'(\\d+ to \\d+)'))) %>%
  reduce(rbind) %>%
  group_by(`EmployerId`) %>%
  mutate('EmployerName' = max(if_else(`Year`== max(`Year`), `EmployerName`, '')), 
         'Pay Gap' = case_when(`DiffMedianHourlyPercent`==0 ~ "In this organisation, men's and women's median hourly pay is equal.", 
                               TRUE ~ paste0("In this organisation, women's median hourly pay is ",
                                             abs(`DiffMedianHourlyPercent`),
                                             "% ",
                                             if_else(`DiffMedianHourlyPercent`>0, 'lower', 'higher'),
                                             " than men's."))) %>%
  select(c('Year', 'Report', 'EmployerName', 'EmployerId', 'EmployerSize', 'DiffMedianHourlyPercent', 'Pay Gap'))

View(final)
