library(dplyr)
library(readr)
library(lubridate)

allFiles <- list.files(path="E:/PD16/", full.names = TRUE, pattern = "^Sales")
temp <- lapply(allFiles, read_csv, col_types =cols(`Email` = col_character(),
                                                   `Order Total` = col_double(),
                                                   `Order Date` = col_date(format = "%d-%b-%Y")))

final <-do.call(rbind, temp) %>%
  filter(`Order Date`>= as.Date("2019/5/24") %m+% months(-6)) %>%
  group_by(`Email`) %>%
  summarise(`Order Total`=sum(`Order Total`)) %>%
  arrange(desc(`Order Total`)) %>%
  mutate('Last 6 Months Rank' = row_number()) %>%
  slice(seq_len(as.integer(n()*0.08)))

View(final)

