library(dplyr)
library(readr)

Sys.setlocale("LC_ALL","English")

final <- read_csv("C:/Data/PreppinData/PD 2022 Wk 1 Input - Input.csv", 
                  col_types = cols(`Date of Birth` = col_date(format = "%m/%d/%Y"))) %>%
  select(c('pupil last name', 'pupil first name', 'Date of Birth')) %>%
  mutate("Pupil\'s Name" = paste(`pupil first name`, `pupil last name`),
         "This Year's Birthday" = `year<-`(`Date of Birth`, 2022),
         "Month" = strftime(`This Year's Birthday`, '%B'),
         "Weekday" = strftime(`This Year's Birthday`, '%A'),
         "Cake Needed On" =  replace(`Weekday`, `Weekday` %in% c("Saturday","Sunday"), "Friday")) %>%
  group_by(`Month`, `Cake Needed On`) %>%
  mutate("BDs per Weekday and Month" = n()) %>%
  select(c("Pupil's Name", "Date of Birth", "This Year's Birthday", "Month", "Cake Needed On", "BDs per Weekday and Month"))
  
View(final)
