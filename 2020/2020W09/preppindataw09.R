library(dplyr)
library(tidyr)
library(readxl)
library(stringr)
library(fuzzyjoin)
library(purrr)

input <- "E:/PD 2020 Wk 8 Input Not Random.xlsx"

sales <-  input %>% excel_sheets() %>% set_names() %>% .[grepl('^Week',.)] %>%
  map_df(~ read_excel(path = input, sheet = .x) %>%
           rename('Sales Volume'=!!names(.[3]),'Sales Value'=!!names(.[4])),.id='Week') %>%
  mutate('Type' = tolower(`Type`),
         'Week' = as.integer(str_extract(`Week`,'\\d+'))) %>%
  group_by(`Type`,`Week`) %>%
  summarise('Sales Volume'=sum(`Sales Volume`),
            'Sales Value'=sum(`Sales Value`))

profit <- read_excel(input, sheet = 'Budget', range = 'C3:F19') %>%
  mutate('Type' = tolower(`Type`),
         'Week' = as.integer(str_extract(`Week`,'\\d+$'))) 

budget <- read_excel(input, sheet = 'Budget', range = 'C22:G26') %>%
  pivot_longer(cols = -c('Type','Measure'), names_to = 'Range', values_to = 'Budget') %>%
  mutate('Range' = as.Date(as.integer(`Range`), origin = '1899-12-30'),
         'From Week' = as.integer(format(`Range`,format='%d')),
         'To Week' = as.integer(format(`Range`,format='%m'))) %>%
  mutate('Type'= str_extract(tolower(`Type`),'[a-z]+'),
         'Measure' = str_remove(`Measure`,'^Budget\\s')) %>%
  pivot_wider(names_from = 'Measure', values_from = 'Budget')

finalA <- fuzzy_inner_join(sales,budget,
                           by=c('Type','Week'='From Week','Week'='To Week'),
                           match_fun=list(`==`,`>=`,`<=`)) %>%
  filter(`Sales Volume`<`Volume` | `Sales Value`<`Value`) %>%
  rename('Type'='Type.x') %>%
  select(c('Type', 'Week', 'Sales Volume', 'Sales Value', 'Volume','Value'))

finalB <- fuzzy_inner_join(sales,profit,
                           by=c('Type','Week','Sales Volume'='Profit Min Sales Volume',
                                'Sales Value'='Profit Min Sales Value'),
                           match_fun=list(`==`,`==`,`>`,`>`)) %>%
  rename('Type'='Type.x','Week'='Week.x') %>%
  select(c('Type', 'Week', 'Sales Volume', 'Sales Value', 'Profit Min Sales Volume','Profit Min Sales Value'))

View(finalA)
View(finalB)
