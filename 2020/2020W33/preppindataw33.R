library(dplyr)
library(readxl)
library(lubridate)
library(tidyr)

xlsx <- "F:/Data/2020W33.xlsx"

final <- read_excel(xlsx, sheet = 'Daily Sales', col_types = c("date", 
                                                               "text", "numeric")) %>%
  merge(read_excel(xlsx, sheet = 'Scent'), by='Scent Code') %>%
  mutate('Week Start' = floor_date(`Date` %m+% days(-3), unit='week') %m+% days(3),
         'Units Sold' = `Daily Sales`/`Price`) %>%
  group_by(`Week Start`, `Scent`) %>%
  summarise('Cost' = max(`Cost`),
            'Weekly Units Sold' = sum(`Units Sold`),
            'Weekly Sales' = sum(`Daily Sales`)) %>%
  merge(read_excel(xlsx, sheet = 'Orders'), by.x='Week Start', by.y='Date', all.x=TRUE) %>%
  mutate_at(vars('Units Ordered'), ~replace_na(., 0)) %>%
  mutate('Waste' = `Units Ordered` - `Weekly Units Sold`,
         'Waste Cost' = `Waste`*`Cost`,
         'Profit' = `Weekly Sales`-`Waste Cost`) %>%
  group_by(`Scent`) %>%
  summarise('Total Profit' = sum(`Profit`)) %>%
  mutate('Profitability Rank' = rank(desc(`Total Profit`)))
  
View(final)