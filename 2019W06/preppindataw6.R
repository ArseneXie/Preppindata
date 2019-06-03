library(readxl)
library(dplyr)
library(lubridate)

new_sales <- read_excel("E:/Week6Input.xlsx", 
                        sheet = "England - Mar 2019") %>%
  mutate('Type of Soap'= sub('^(.*) Soap','\\1',`Category`),
         'Month'= format(as.Date("2019-03-01", "%Y-%m-%d"), format="%b %y"))  
price_dtl <- read_excel("E:/Week6Input.xlsx", 
                        sheet = "Soap Pricing Details") 
com_data <- read_excel("E:/Week6Input.xlsx", 
                       sheet = "Company Data") %>%
  mutate('Month'= format(`Month`, format="%b %d"))

final <- new_sales %>%
  merge(., price_dtl, by='Type of Soap') %>%
  group_by(`Month`,`Country`,`Category`) %>% 
  summarise('Profit'= sum(`Units Sold`*(`Selling Price per Unit`-`Manufacturing Cost per Unit`))) %>%
  ungroup %>%
  rbind(com_data,.)

View(final)