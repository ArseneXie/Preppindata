library(readr)
library(dplyr)

Sys.setlocale("LC_ALL","English")

final <- read_csv("C:/Data/PreppinData/PD 2021 Wk 49 Input - Input.csv",
                  col_types =cols(`Date` = col_date(format = "%d/%m/%Y"))) %>%
  group_by(`Name`) %>%
  arrange(`Date`) %>%
  mutate('Report Year' = strftime(`Date`,'%Y'),
         'Employment Range' = paste(strftime(min(`Date`),'%b %Y'),'to',strftime(max(`Date`),'%b %Y')),
         'Months Count' = 1, 
         'Nth Month' = cumsum(`Months Count`)) %>%
  group_by(`Name`, `Report Year`) %>%
  summarise('Employment Range' = first(`Employment Range`),
            'Tenure by End of Reporting Year' = max(`Nth Month`),
            'Salary Paid' = round(first(`Annual Salary`)*sum(`Months Count`)/12,2),
            'Yearly Bonus' = sum(`Sales`)*0.05,
            'Total Paid' = round(`Salary Paid`+`Yearly Bonus`), .groups='drop') %>%
  select(c('Name', 'Employment Range', 'Report Year', 
           'Tenure by End of Reporting Year', 'Salary Paid', 'Yearly Bonus', 'Total Paid'))

View(final)
