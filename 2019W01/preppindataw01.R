library(readxl)
library(dplyr)

final <- read_excel("E:/Week 1 Input.xlsx", 
                    col_types = c("text", "numeric", "numeric", 
                                  "numeric", "numeric", "numeric", "numeric", 
                                  "skip", "skip", "skip", "skip")) %>%
  mutate('Date' = as.Date(paste(`When Sold Year`,`When Sold Month`,'01', sep='-')),
         'Total Cars Sold' = `Red Cars`+`Silver Cars`+`Black Cars`+`Blue Cars`) %>%
  select(-c('When Sold Year','When Sold Month'))

View(final)