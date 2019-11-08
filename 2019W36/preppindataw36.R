library(dplyr)
library(tidyr)
library(readr)
library(stringr)

convert_ht <- function(df){
  df %>%
    mutate('ft'= as.integer(str_extract(`HT`,'^(\\d+)')),
           'inch' = as.integer(str_extract(`HT`,'\\s(\\d+)')),
           'Height (m)' = round((`ft`*12+`inch`)*2.54/100,2)) %>%
    select(-c('HT','ft','inch'))
}  

convert_wt <- function(df){
  df %>%
    mutate('lbs'= as.integer(str_extract(`WT`,'^(\\d+)')),
           'Weight (KGs)' = round(`lbs`*0.453592,2)) %>%
    select(-c('WT','lbs'))
}  

jersey_no <- function(df){
  df %>%
    mutate('NAME' = str_replace(`NAME`,'(\\d+)',',\\1')) %>%
    separate(`NAME`,c('NAME','Jersey Number'),sep=',',convert=TRUE)
}  

proc_all <- function(df){
  df %>% convert_ht(.) %>% convert_wt(.) %>% jersey_no(.)
}

spurs <- read_csv("E:/PD - Week 36 - Data.csv") %>% proc_all(.) 
nets <- read_csv("E:/PD - Week 36 - Brooklyn Data.csv") %>% proc_all(.) 

View(spurs)
View(nets)