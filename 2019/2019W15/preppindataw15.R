library(dplyr)
library(readr)

allFiles <- list.files(path="E:/PD15/", full.names = TRUE, pattern = "Stock Purchases.csv$")
temp <- lapply(allFiles, read_csv, col_types =cols(`Customer ID` = col_double(),
                                                    `First Name` = col_character(),
                                                    `Last Name` = col_character(),
                                                    Sales = col_double(),
                                                    `Order Date` = col_character(),
                                                    Stock = col_character()))
names(temp) <- sub('.*PD15/(\\w+)\\s.*','\\1', allFiles)
for(i in names(temp)) 
  temp[[i]]$Region = i

final <-do.call(rbind, temp) %>%
  group_by(`Stock`,`Region`) %>%
  mutate('Total Regional Sales' = sum(`Sales`),
         '% of Total Regional Sales' = `Sales`/sum(`Sales`)*100) %>%
  group_by(`Stock`) %>%
  mutate('Total Sales' = sum(`Sales`),
         '% of Total Sales' = `Sales`/sum(`Sales`)*100) %>%
  filter(`% of Total Regional Sales`< 100) 

View(final)

#check <- final %>%
#  filter(`Region`=='South' & `Customer ID`=='1')
