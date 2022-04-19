library(readr)
library(dplyr)

final <- read_csv("C:/Data/PreppinData/PD Fill the Blanks challenge.csv") %>%
  group_by(`Weekday`, `Lesson Time`) %>%
  mutate('Lesson Name' = max(`Lesson Name`, na.rm = TRUE),
         'Subject' = max(`Subject`, na.rm = TRUE)) %>%
  group_by(`Weekday`, `Lesson Name`, `Subject`) %>%
  mutate('Avg. Attendance per Subject & Lesson' = mean(`Attendance`)) 
  
View(final)
