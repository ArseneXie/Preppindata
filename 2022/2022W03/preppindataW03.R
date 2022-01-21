library(dplyr)
library(tidyr)
library(readr)

final <- read_csv("C:/Data/PreppinData/PD 2022 Wk 1 Input - Input.csv") %>%
  select(c('id', 'gender')) %>%
  `colnames<-`(c('Student ID','Gender')) %>%
  merge(read_csv("C:/Data/PreppinData/PD 2022 WK 3 Grades.csv"), by='Student ID') %>%
  pivot_longer(col=-c('Student ID','Gender'), names_to='Subject', values_to = 'Score') %>%
  group_by(`Student ID`, `Gender`) %>%
  summarise("Student's Avg Score" = round(mean(`Score`),1),
            "Passed Subjects" = sum(`Score`>=75), .groups = "drop") %>%
  select(c('Passed Subjects', "Student's Avg Score", 'Student ID', 'Gender'))
  
View(final)
