library(dplyr)
library(readr)
library(openxlsx)

Complaints <- read_csv("F:/Data/Prep Air Complaints - Complaints per Day.csv", 
                       col_types = cols(Date = col_date(format = "%d/%m/%Y"))) %>%
  group_by(`Week`) %>%
  mutate('Mean' = mean(`Complaints`),
         'Standard Deviation' = sd(`Complaints`))

NSD <- function(N){
  df <-Complaints %>%
    mutate('Lower Control Limit' = `Mean`-`Standard Deviation`*N,
           'Upper Control Limit' = `Mean`+`Standard Deviation`*N,
           'Variation' = `Upper Control Limit`-`Lower Control Limit`,
           'Outlier' = if_else(`Upper Control Limit`>=`Complaints` & `Complaints`>=`Lower Control Limit`,'Inside','Outside')) %>%
    filter(`Outlier`=='Outside')
  return(df)
}

fin_sheet <- list("1SD" = NSD(1), "2SD" = NSD(2), "3SD" = NSD(3))
write.xlsx(fin_sheet, file = "F:/Data/prepindata2021w20r.xlsx")
