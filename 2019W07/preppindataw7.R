library(readxl)
library(dplyr)

deptdtl <- read_excel("E:/Week7Challenge.xlsx", 
                           sheet = "Departure Details", col_types = c("text", 
                                                                      "date", "numeric", "numeric"))

allcdtl <- read_excel("E:/Week7Challenge.xlsx", 
                            sheet = "Allocation Details", col_types = c("text", 
                                                                        "text", "date", "text", "numeric", 
                                                                        "numeric"))

final <- deptdtl %>%
      mutate("Departure ID" = paste0(`Ship ID`,"-",format(`Departure Date`, format="%d-%m-%Y"))) %>%
      merge(., allcdtl, by="Departure ID") %>%
      group_by(`Ship ID`,`Departure Date`) %>% 
      summarise("Max Weight"= max(`Max Weight`),
                "Max Volume"= max(`Max Volume`),
                "Weight Allocated"= sum(`Weight Allocated`),
                "Volume Allocated"= sum(`Volume Allocated`)) %>%
      mutate("Weight Exceeded" = `Weight Allocated`>`Max Weight`,
             "Volume Exceeded" = `Volume Allocated`>`Max Volume`,
             "Departure Date" = format(`Departure Date`,format="%d/%m/%Y")) 


View(final)