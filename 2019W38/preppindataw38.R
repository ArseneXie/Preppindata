library(dplyr)
library(readr)

visit <- read_csv("E:/Input Data.csv", 
                  col_types = cols(`Date of Servce` = col_date(format = "%m/%d/%Y"))) %>%
  group_by(`PatientID`) %>%
  arrange(`Date of Servce`) %>%
  mutate('Patient Visit Number' = cumsum(`PatientID`/`PatientID`),
         'First Visit Date' = min(`Date of Servce`),
         'Total Patient Visits' = max(`Patient Visit Number`),
         'New Patient Flag' = ifelse(`Patient Visit Number`==1,'New Patient','Returning Patient'))
  
View(visit)

#check <- visit %>% filter(`PatientID`==94)