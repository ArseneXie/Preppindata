library(googlesheets4)
library(googledrive)
library(dplyr)
library(purrr)
library(stringr)

google_sheet <- drive_get('Taipei Weather Data') 

final <- as.vector(sheet_properties(google_sheet)[['name']]) %>%
  set_names() %>%
  map_df(~ read_sheet(google_sheet[['id']],sheet = .x),.id = 'Forecast Type') %>%
  mutate('Data' = str_replace_all(`Data`,'\\n','|'),
         'Date or Time' = str_extract(`Data`, '^([^|]*)|'),
         'Temperature' = as.integer(str_extract(str_replace_all(`Data`,'(\\|\\d+¢X){2}',''),'(?<=\\|)(\\d+)(?=¢X)')),
         'Precipitation Chance'= as.integer(str_extract(`Data`,'(?<=\\|)(\\d+)(?=%)')),
         'Max Temp' = as.integer(str_extract(`Data`,'(?<=\\|)(\\d+)(?=¢X\\|\\d+¢X)')),
         'Min Temp' = as.integer(str_extract(`Data`,'(?<=¢X\\|)(\\d+)(?=¢X)'))) %>%
  select(-'Data')

View(final)