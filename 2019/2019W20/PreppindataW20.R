library(readxl)
library(dplyr)
library(tidyr)
library(fuzzyjoin)
library(lubridate)

clean_range <- function(rg){
  sapply(rg,function(rg){
    if (grepl('.*-.*',rg)){
      return(rg)
    } else {
      td <- as.Date(as.numeric(rg),origin = "1899-12-30")
      return(paste0(as.character(day(td)),'-',as.character(month(td))))
    }  
  })
}

patient <- read_excel("E:/PD - Week 20.xlsx", 
                      sheet = "Patient", col_types = c("text", 
                                                       "date", "numeric"))
cost_per_visit <- read_excel("E:/PD - Week 20.xlsx", 
                             sheet = "Cost per Visit", col_types = c("text", 
                                                                     "numeric")) %>%
  mutate('Length of Stay' = clean_range(`Length of Stay`)) %>%
  separate(`Length of Stay`, c('From', 'To')) %>%
  mutate('Times' = as.integer(`To`) - as.integer(`From`)+1) %>%
  select(c('Cost per Day','Times'))
  
cost <- cost_per_visit[rep(seq(nrow(cost_per_visit)), cost_per_visit$Times),] %>%
  mutate('nday'=seq.int(nrow(.)))
  
rawdata <- fuzzy_inner_join(patient,cost,
                          by=c('Length of Stay' = 'nday'),
                          match_fun = list(`>=`)) %>%
  mutate('Date' = `First Visit` %m+% days(`nday`-1))

finalA <- rawdata %>%
  group_by(`Name`) %>%
  summarise('Cost' = sum(`Cost per Day`),
            'Avg Cost per day per person'=mean(`Cost per Day`))
  
finalB <- rawdata %>%
  group_by(`Date`) %>%
  summarise('Avg Cost per day'=mean(`Cost per Day`),
            'Cost per Day' = sum(`Cost per Day`),
            'Number of patients' = n())

View(finalA)
View(finalB)
