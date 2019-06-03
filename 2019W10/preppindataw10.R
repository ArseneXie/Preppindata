library(readxl)
library(dplyr)
library(fuzzyjoin)
library(lubridate)

sign_up <- read_excel("E:/PD - Week 10 - Email Subscriptions.xlsx", 
                      sheet = "Mailing List 2018", col_types = c("text", 
                                                                 "numeric", "numeric", "date")) %>%
  rename("Interested in Liquid Soap" = "Liquid",
         "Interested In Soap Bars" = "Bar") %>%
  mutate_at("Sign-up Date",as.Date) 

unsub <- read_excel("E:/PD - Week 10 - Email Subscriptions.xlsx", 
                    sheet = "Unsubscribe list", col_types = c("text", 
                                                              "text", "text")) %>%
         mutate('Unsubscribe Date'=as.Date(`Date`, "%d.%m.%Y")) %>%
         mutate('possible key'=paste0('^',tolower(substr(`first_name`,1,1)),gsub('[^a-z]','',tolower(`last_name`)))) %>%
         select(-c("Date","first_name","last_name"))
         
lifetime_val <- read_excel("E:/PD - Week 10 - Email Subscriptions.xlsx", 
                           sheet = "Customer Lifetime Value")

signup_lifeval <- sign_up %>%
  merge(., lifetime_val, by='email') 

sub_wi_unsub <- signup_lifeval %>%  
  regex_inner_join(unsub, by = c(`email` = 'possible key')) %>%
  select(-'possible key') %>%
  mutate('Status' = ifelse(`Unsubscribe Date`>`Sign-up Date`,'Unsubscribed','Resubscribed'))

sub_wo_unsub <- signup_lifeval %>%  
  regex_anti_join(unsub, by = c(`email` = 'possible key')) %>%
  mutate('Unsubscribe Date' = as.Date(NA)) %>%
  mutate('Status' = 'Subscribed') 

finalA <- rbind(sub_wo_unsub,
                sub_wi_unsub %>% filter(.,Status=='Resubscribed')) 
                
finalB <- rbind(sub_wo_unsub,sub_wi_unsub) %>%
  mutate('months' = time_length(`Unsubscribe Date`-`Sign-up Date`, "month")) %>%
  mutate('months before unsubscribe' = case_when(
    `months` >= 0 & `months` <= 3 ~ '0-3',
    `months` > 3 & `months` <= 6 ~ '3-6',
    `months` > 6 & `months` <= 12 ~ '6-12',
    `months` > 12 & `months` <= 24 ~ '12-24',
    `months` > 24 ~ '24+', 
    TRUE ~ as.character(NA)
  )) %>%
  select(-c('months','Unsubscribe Date','Sign-up Date')) %>%
  group_by(`months before unsubscribe`,`Status`,`Interested in Liquid Soap`,`Interested In Soap Bars`) %>% 
  summarize("email"=  n(),
          "Liquid Sales to Date"= sum(`Liquid Sales to Date`),
          "Bar Sales to Date"= sum(`Bar Sales to Date`)) 
  
View(finalB)
View(finalA)