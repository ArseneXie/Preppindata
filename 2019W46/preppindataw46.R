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
  group_by()

  


all_list<- c('Nice List','Naughty List') %>%
  set_names() %>%
  map_df(~ read_excel(path = input, sheet = .x,),.id = 'List') %>%
  rename('Name Part' = 'Name') 

present <- read_excel(input, sheet = 'Present List') %>% 
  rename('Address Part' = 'Address') 


c <- regex_inner_join(all_list,present,by = c('Address'='Address Part')) %>%
  merge(.,regex_inner_join(present,all_list,by = c('Name'='Name Part')),
        by=c('List','Name','Address')) %>%
  distinct() 

join_list <- c('Nice List','Naughty List') %>%
  set_names() %>%
  map_df(~ read_excel(path = input, sheet = .x,),.id = 'List') %>%
  regex_inner_join(read_excel(input, sheet = 'Present List'), 
                   by = c('N'))
  

input <- "E:/2019 PD Wk 46.xlsx"

final <-  input %>%
  excel_sheets() %>%
  set_names() %>%
  map_df(
    ~ read_excel(path = input, sheet = .x,),
    .id = "sheet name") %>%

final <- read_excel("E:/Week Two Input.xlsx", 
                    col_types = c("text", "text", "text", 
                                  "numeric", "date")) %>%
  drop_na() %>%
  mutate('City' = if_else(grepl('.*gh$',`City`),'Edinburgh','London')) %>%
  unite('R2CHdr',`Metric`,`Measure`, sep=' - ') %>%
  spread(`R2CHdr`,`Value`)

View(final)

final <-  c('Nice List','Naughty List') %>%
  set_names() 