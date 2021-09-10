library(readxl)
library(dplyr)
library(tidyr)
library(stringi)

input <- "F:/Data/2021 Week 34 Input.xlsx"

final <- read_excel(path = input, sheet = 'Employee Sales') %>%
  pivot_longer(cols=-c('Store', 'Employee'), names_to='Month', values_to = 'Monthly Sales') %>%
  group_by(`Store`, `Employee`) %>%
  mutate('Avg monthly Sales' = round(mean(`Monthly Sales`))) %>%
  merge(., read_excel(path = input, sheet = 'Employee Targets') %>%
          mutate('Store' = stri_replace_all_regex(`Store`, pattern = c('^B.*', '^S.*', '.imble.*', '^Y.*'),
                                                  replacement = c('Bristol', 'Stratford', 'Wimbledon', 'York'),
                                                  vectorize_all = FALSE)),
        by = c('Store', 'Employee')) %>%
  filter(`Avg monthly Sales`<`Monthly Target`*0.9) %>%
  group_by(`Store`, `Employee`) %>%
  summarise('Avg monthly Sales' = first(`Avg monthly Sales`),
            '% of months target met' = round(sum(if_else(`Monthly Sales`>=`Monthly Target`,1,0))/n()*100),
            'Monthly Target' = first(`Monthly Target`),
            .groups = 'drop')

View(final)
