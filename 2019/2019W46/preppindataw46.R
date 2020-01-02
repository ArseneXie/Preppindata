library(readxl)
library(dplyr)
library(tidyr)
library(purrr)
library(fuzzyjoin)

input <- "E:/2019 PD Wk 46.xlsx" 

join_list <- c('Nice List','Naughty List') %>%
  set_names() %>%
  map_df(~ read_excel(path = input, sheet = .x,),.id = 'List') %>%
  rename('Name Part' = 'Name') %>%
  regex_inner_join(read_excel(input, sheet = 'Present List') %>% 
                     rename('Address Part' = 'Address') , 
                   by = c(`Address`='Address Part')) %>%
  filter(mapply(grepl,`Name Part`,`Name`)) 

detail_list <- join_list %>%
  group_by(`List`,`Name`,`Address`,`Family Role`,`Item`) %>%
  summarise('Elves Build Time (min)'=max(`Elves Build Time (min)`),
            'Reason'=last(`Reason`)) 

summary <- detail_list %>%
  group_by(`List`) %>%
  summarise('Total Hours Build Time'= round(sum(`Elves Build Time (min)`)/60)) 

missing_list <- anti_join(read_excel(input, sheet = 'Present List'),join_list,
                          by=c('Name','Address'='Address Part'))  

View(summary)
View(detail_list)
View(missing_list)