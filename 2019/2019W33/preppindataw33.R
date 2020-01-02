library(readxl)
library(dplyr)
library(tidyr)
library(purrr)
library(fuzzyjoin)
library(lubridate)

input <- "E:/PD Wk33.xlsx"
emp_sal <-  input %>%
  excel_sheets() %>% .[grepl('.*Store$',.)] %>%
  set_names() %>%
  map_df(
    ~ read_excel(path = input, sheet = .x,),
    .id = 'Store') %>%
  mutate_at(vars('End Date'), ~replace_na(.,as.Date('2019/10/1'))) %>%
  filter(as.Date(`End Date`) >= as.Date('2019/1/1')) 

sal_range <- read_excel(path = input, 
                        sheet = "Salary Range") %>%
  separate(`Range`,c('Salary Range Minimum', 'Salary Range Maximum'),sep='-',remove =FALSE) %>%
  mutate_at(vars('Bonus amount','Salary Range Minimum','Salary Range Maximum'),
            ~(function(x) as.integer(gsub('[^0-9]','',x)))(.)) %>%
  mutate('Ranking' =  dense_rank(`Salary Range Maximum`),
         'Assumed Position Based on Salary Range' = case_when(
           `Ranking` == 1 ~ 'Team Member',`Ranking` == 2 ~ 'Manager',`Ranking` == 3 ~ 'Area Manager')) %>%
  select(-'Ranking')

emp_bns <- fuzzy_left_join(emp_sal, sal_range, 
                           by = c('Salary'='Salary Range Minimum','Salary'='Salary Range Maximum'),
                           match_fun = list(`>=`, `<=`)) %>%
  mutate_at(vars('Bonus amount'), ~replace_na(.,0))

final1 <- emp_bns %>%
  mutate('Pay Stuts' = if_else(is.na(`Range`),'Incorrect Pay','Assumed Coreect Pay'),
         'Correct Salay for Role' = if_else(is.na(`Assumed Position Based on Salary Range`),
                                                  FALSE,`Role`== `Assumed Position Based on Salary Range`)) %>%
  filter(!`Correct Salay for Role`)

sales <- read_excel(path = input, 
                        sheet = "Store Sales") %>%
  gather('SalesDate', 'MonSales', -c('Store','Quarterly Target')) %>% 
  mutate('SalesDate' = floor_date(as.Date(as.numeric(`SalesDate`), origin = '1899-12-30'),'quarter') %m+% months(2),
         'Store_dup' = paste(`Store`,'Store')) %>%
  group_by(`Store_dup`,`SalesDate`) %>%
  summarise('Qsales'=sum(`MonSales`), 'Target'=max(`Quarterly Target`)) %>%
  filter(`Qsales`>=`Target`) %>%
  select(c('Store_dup','SalesDate'))

final2 <- fuzzy_inner_join(emp_bns, sales, 
                           by = c('Store'='Store_dup','Start Date'='SalesDate','End Date'='SalesDate'),
                           match_fun = list(`==`,`<=`, `>=`)) %>%
  
  group_by(`Store`,`Name`,`Salary`) %>%
  summarise('Bonus amount' = sum(`Bonus amount`)) %>%
  mutate('% Bonus of Salary'=`Bonus amount`/`Salary`*100)
