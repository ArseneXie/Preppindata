library(readxl)
library(dplyr)
library(stringr)

xlsx <- "C:/Data/PreppinData/2022W17 Input.xlsx"

final <-  read_excel(xlsx, 'Streaming') %>%
  mutate('location' = str_replace(`location`, '^Edin.*', 'Edinburgh'), 
         'timestamp' = as.POSIXct(str_replace_all(`t`, '[A-Z]', ' ')),
         'content_type' = if_else(str_detect(`location`,'(London|Cardiff|Edinburgh)'),'Primary',
                                  if_else(is.na(`content_type`),'Secondary', `content_type`))) %>%
  group_by(`userID`, `timestamp`, `location`, `content_type`) %>%
  summarise('duration' = sum(`duration`), .groups='drop') %>%
  mutate('dummy_location' = if_else(`content_type`=='Primary', 'dummy',`location`)) %>%
  group_by(`userID`, `dummy_location`, `content_type`) %>%
  mutate('Month' = format(min(`timestamp`), '%m %Y')) %>%
  merge(read_excel(xlsx, 'Avg Pricing') %>% rename('content_type'='Content_Type'), by=c('Month','content_type'), all.x = TRUE) %>%
  mutate('Avg_Price' = if_else(`content_type`=='Preserved', 14.98, `Avg_Price`)) %>%
  select(c('userID', 'timestamp', 'location', 'content_type', 'duration', 'Avg_Price'))
  
View(final)
