library(readxl)
library(dplyr)
library(lubridate)

df <- read_excel("H:/PreppinData - Week Three.xlsx", 
                           sheet = "Contract Details", col_types = c("text", 
                                                                     "numeric", "numeric", "date"))

final <- df[rep(seq_len(nrow(df)), df[['Contract Length (months)']]),] %>%
   group_by(`Name`) %>%
   mutate(counter = row_number(`Name`)) %>%
   mutate('Payment Date' = `Start Date` %m+% months(counter-1)) %>%
   select(c('Payment Date','Name','Monthly Cost','Contract Length (months)','Start Date'))
   
View(final)