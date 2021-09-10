library(readxl)
library(dplyr)
library(tidyr)
library(stringr)
library(fuzzyjoin)

input <- "F:/Data/Pictures Input.xlsx"

analyze_size <- function(size_str) {
  convert <- if_else(str_detect(size_str,'(cm)'),1.0,2.54)
  side_a <- as.numeric(str_extract(size_str,'^(\\d+)'))*convert
  side_b <- if_else(str_detect(size_str,'(?<=\\D)(\\d+)(?=\\D)'),
                    as.numeric(str_extract(size_str,'(?<=\\D)(\\d+)(?=\\D)'))*convert, side_a)
  return(paste(sort(c(side_a, side_b, side_a*side_b)), collapse = ','))
}

picture <- read_excel(path = input, sheet = 'Pictures') %>%
  rowwise() %>%
  mutate('Side all' = analyze_size(`Size`)) %>%
  separate(`Side all`, c('Min Side', 'Max Side', 'Area'), sep=',', convert=TRUE)

frame <- read_excel(path = input, sheet = 'Frames') %>%
  rowwise() %>%
  mutate('Side all' = analyze_size(`Size`)) %>%
  separate(`Side all`, c('Frame Min Side','Frame Max Side', 'Frame Area'), sep=',', convert=TRUE) %>%
  rename('Frame' = 'Size')
  
final <- fuzzy_inner_join(picture, frame, 
                          by = c('Min Side'='Frame Min Side','Max Side'='Frame Max Side'), match_fun = list(`<=`, `<=`)) %>%
  group_by(`Picture`) %>%
  filter(`Frame Area`-`Area` == min(`Frame Area`-`Area`)) %>%
  select(c('Picture', 'Frame', 'Max Side', 'Min Side'))

View(final)
