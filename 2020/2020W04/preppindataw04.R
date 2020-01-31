library(dplyr)
library(tidyr)
library(readr)
library(stringr)
library(lubridate)

clean_country <- function(x) {
  return(if_else(str_detect(x,'(?i)(gland)'),'England',
                 if_else(str_detect(x,'(?i)(^sc)'),'Scotland',
                         if_else(str_detect(x,'(?i)(Netherland)'),'Netherlands',
                                 if_else(str_detect(x,'(?i)(United)'),'United States',x)))))
}
get_ymd_date <- function(x) {
  draft <- str_replace_all(str_replace(str_replace(str_replace_all(str_replace(x,
                                                                               '(.*\\D$)','\\1 2020'),
                                                                   '\\s',''),
                                                   '(^.*)(?:Jan)(.*$)','\\1/01/\\2'),
                                       '(^.*)(?:Dec)(.*$)','\\1/12/\\2'),
                           '\\D+','@')
  return(if_else(str_detect(draft,'(@*\\d+@*((0?[1-9])|(1[0-2]))@*\\d{4})'),
                 str_replace(draft,'(?:@*)(\\d+)(?:@*)(\\d+)(?:@*)(\\d+)','\\3/\\2/\\1'),
         if_else(str_detect(draft,'(@*((0?[1-9])|(1[0-2]))@*\\d+@*\\d{4})'),
                 str_replace(draft,'(?:@*)(\\d+)(?:@*)(\\d+)(?:@*)(\\d+)','\\3/\\1/\\2'),
         if_else(str_detect(draft,'(@*\\d{4}@*((0?[1-9])|(1[0-2]))@*\\d+)'),
                 str_replace(draft,'(?:@*)(\\d+)(?:@*)(\\d+)(?:@*)(\\d+)','\\1/\\2/\\3'),draft))))
}
get_time_str <- function(x) {
  return(paste0(str_pad(as.integer(str_extract(str_replace_all(x,'\\D',''),'(\\d+)(?=\\d{2})'))
                        +if_else(str_detect(x,'(p|P)'),12,0),2,'left','0'),':',
                str_extract(str_replace_all(x,'\\D',''),'(\\d{2}$)')))
}
final <- read_csv("E:/PD 2020 Wk 4 Input.csv") %>%
  group_by(`Question Number`) %>% 
  mutate('Id' = row_number()) %>%
  merge(.,read_csv("E:/Store Survey Results - Question Sheet.csv"), by.x='Question Number', by.y='Number') %>%
  select(-'Question Number') %>%
  spread('Question','Answer') %>%
  rowwise() %>%
  mutate('Country' = clean_country(`Country`),
         'Date' = get_ymd_date(`What day did you fill the survey in?`),
         'Time' = get_time_str(`What time did you fill the survey in?`),
         'Completion Date' = as.POSIXct(paste0(`Date`,' ',if_else(`Time`=='24:00','00:00',`Time`)), format = "%Y/%m/%d %H:%M")
                             +days(if_else(`Time`=='24:00',1,0)),
         'Age of Customer' = 2020-as.integer(str_extract(`DoB`,'(\\d+$)')),
         'Score' = as.integer(`Would you recommend C&BSco to your friends and family? (Score 0-10)`)) %>%
  ungroup() %>%
  group_by(`Country`,`Store`,`Name`) %>%
  mutate('Result' = if_else(rank(`Completion Date`)==1,'First',if_else(rank(desc(`Completion Date`))==1,'Latest','Drop')),
         'NPS' = if_else(`Score`<=6,'Detractor',if_else(`Score`>=9,'Promoter','Passive')),
         'Value' = 1) %>%
  filter(`Result`!='Drop') %>%
  spread('NPS','Value') %>%
  select(c('Country', 'Store', 'Name','Completion Date','Result',
           'Would you recommend C&BSco to your friends and family? (Score 0-10)','Promoter','Detractor','Passive',
           'Age of Customer','If you would, why?',"If you wouldn't, why?"))
View(final)