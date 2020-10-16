library(dplyr)
library(readxl)
library(stringr)
library(purrr)
library(lubridate)

input <- "F:/Data/Prep Tips live chat logs.xlsx"
data <-  input %>%
  excel_sheets() %>%
  set_names() %>%
  map_df(
    ~ read_excel(path = input, sheet = .x),
    .id = 'Location') %>%
  mutate('Location' = str_extract(`Location`,'^(\\w+)'),
         'Date (GMT)' = as.POSIXct(paste('2020-10-07',format(`Time`, '%H:%M:%S')),format='%Y-%m-%d %H:%M:%S')
         +hours(case_when(`Location`=='APAC'~-11,`Location`=='EMEA'~-1,`Location`=='AM'~5))) %>%
  group_by(`Location`,`Who`) %>%
  mutate('Seq' = row_number(`Date (GMT)`),
         'Category' = if_else(`Seq`==1,'Intro',if_else(str_detect(`Comment`,'(\\?)$'),'Question','Answer'))) %>%
  filter(!((`Who`=='Carl Allchin') & (`Seq`==1)))

output1 <- data %>%
  filter(`Category`=='Intro') %>%
  mutate('City' = str_extract_all(`Comment`,'^([\\w\\s]+)'),
         'Country' = if_else(`Location`=='AM','United States',trimws(str_extract_all(`Comment`,'(?<=,)([\\w\\s]+)'))),
         'First Time Indicator?' = if_else(str_detect(tolower(`Comment`),'(first time)'),1,0)) %>%
  select('Date (GMT)', 'Location', 'City', 'First Time Indicator?', 'Country', 'Who')

output2 <- data %>%
  filter(!(`Category`=='Intro')) %>%
  rename('Question or Answer'='Category') %>%
  group_by(`Location`,`Question or Answer`) %>%
  summarise('Instances'=n())
  
View(output1)
View(output2)
