library(readxl)
library(dplyr)
library(tidyr)

theft <- read_excel("E:/Week 8 Input.xlsx",
                    sheet = "Theft Audit", col_types = c("text", 
                                                         "text", "date", "numeric", "text", 
                                                         "text")) %>%
         mutate("Type" = if_else(grepl('.*Bar.*',`Type`), 'Bar', `Type`)) %>%
         mutate("Type" = if_else(grepl('^L.*',`Type`), 'Liquit', `Type`))  

branch <- read_excel("E:/Week 8 Input.xlsx", 
                     sheet = "Branch ID") %>%
          separate(`Branch ID`, c("Store ID", "Branch Name"), sep = " - ")

final <- theft %>%
      merge(., branch, by="Store ID") %>%
      select(-("Store ID")) %>%
      mutate_at(vars("Date","Quantity"), as.character) %>%
      gather(., key="var", value="value", "Date", "Quantity") %>%
      unite(newcol, `var`, `Action`) %>%
      spread(newcol, value) %>%
      mutate_at(vars(matches("Date")), as.Date) %>%
      mutate_at(vars(matches("Quantity")), as.numeric) %>%
      mutate_if(is.numeric, ~replace(., is.na(.), 0)) %>% 
      mutate("Days to cmop adj" = `Date_Stock Adjusted`-`Date_Theft`,
             "Stock Variance" =`Quantity_Stock Adjusted`+`Quantity_Theft`) %>%
      rename("Stock Adjusted" = "Date_Stock Adjusted",
             "Theft" = "Date_Theft",
             "Stolen Volume" = "Quantity_Theft") %>%
      select(-("Quantity_Stock Adjusted"))
  
View(final)

