library(readxl)
library(dplyr)
library(lubridate)
library(fuzzyjoin)

xlsx <- "F:/Data/Copy of Karaoke Dataset.xlsx"

final <- read_excel(xlsx, sheet = "Karaoke Choices", col_types = c("date", "text", "text")) %>%
  arrange(`Date`) %>% 
  mutate('Seq' = row_number(),
         'Time between Prev Songs' = round(time_length(`Date`-lag(`Date`),'minutes'),0),
         'Session #' = cumsum(if_else(`Seq`==1 | `Time between Prev Songs`>=59,1,0))) %>%
  group_by(`Session #`) %>%
  mutate('Song Order' = `Seq`-min(`Seq`)+1,
         'Session Start Date' = min(`Date`),
         'Session Early Date' = `Session Start Date` %m+% minutes(-10)) %>%
  fuzzy_left_join(., read_excel(xlsx, sheet = "Customers", col_types = c("text", "date")), 
                  by = c('Session Start Date'='Entry Time','Session Early Date'='Entry Time'),
                  match_fun = list(`>=`, `<=`)) %>%
  select(c('Session #', 'Customer ID', 'Song Order', 'Date', 'Artist', 'Song'))

View(final)
