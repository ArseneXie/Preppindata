library(dplyr)
library(readr)
library(lubridate)

final <- read_csv("C:/Data/PreppinData/PD 2022 Wk 1 Input - Input.csv", 
                  col_types = cols(`Date of Birth` = col_date(format = "%m/%d/%Y"))) %>%
  mutate('Pupil\'s Name' = paste(`pupil last name`, `pupil first name`, sep=', '),
         'parent first name' = if_else(`Parental Contact`==1, `Parental Contact Name_1`, `Parental Contact Name_2`),
         'Parental Contact Full Name' = paste(`pupil last name`, `parent first name`, sep=', '),
         'Parental Contact Email Address' =  paste0(`parent first name`, '.', `pupil last name`, '@', `Preferred Contact Employer`, '.com'),
         'Birth Fiscal Year' = as.integer(quarter(`Date of Birth`,with_year = TRUE, fiscal_start = 9)),
         'Academic Year' = 2016 - if_else(`Birth Fiscal Year`>2015, as.integer(2015), `Birth Fiscal Year`)) %>%
  select(c('Academic Year', 'Pupil\'s Name', 'Parental Contact Full Name', 'Parental Contact Email Address'))
  
View(final)