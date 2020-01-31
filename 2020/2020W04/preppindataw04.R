library(dplyr)
library(tidyr)
library(readr)
library(stringr)

clean_country <- function(x) {
  return(if_else(str_detect(x,'(?i)(gland)'),'England',
                 if_else(str_detect(x,'(?i)(^sc)'),'Scotland',
                         if_else(str_detect(x,'(?i)(Netherland)'),'Netherlands',
                                 if_else(str_detect(x,'(?i)(United)'),'United States',x)))))
}

get_ymd_date <- function(x) {
  draft <- str_replace(x,'(.*\\D$)','\\1 2020')
  return(draft)
}

x = re.sub('\D','@', re.sub('(^.*)(?:Dec)(.*$)',r'\1/12/\2', re.sub('(^.*)(?:Jan)(.*$)',r'\1/01/\2', re.sub('\s','', re.sub('(.*\D$)',r'\1 2020',x)))))
return re.sub('(?:@*)(\d+)(?:@*)(\d+)(?:@*)(\d+)',r'\3/\2/\1',x) if re.search('(@*\d+@*((0?[1-9])|(1[0-2]))@*\d{4})',x) else \
re.sub('(?:@*)(\d+)(?:@*)(\d+)(?:@*)(\d+)',r'\3/\1/\2',x) if re.search('(@*((0?[1-9])|(1[0-2]))@*\d+@*\d{4})',x) else \
re.sub('(?:@*)(\d+)(?:@*)(\d+)(?:@*)(\d+)',r'\1/\2/\3',x) if re.search('(@*\d{4}@*((0?[1-9])|(1[0-2]))@*\d+)',x) else x

temp <- read_csv("E:/Store Survey Results - Question Sheet.csv")

result <- read_csv("E:/PD 2020 Wk 4 Input.csv") %>%
  group_by(`Question Number`) %>% 
  mutate('Id' = row_number()) %>%
  merge(.,read_csv("E:/Store Survey Results - Question Sheet.csv"), by.x='Question Number', by.y='Number') %>%
  spread('Question','Answer') %>%
  rowwise() %>%
  mutate('Country' = clean_country(`Country`),
         'Date' = get_ymd_date(`What day did you fill the survey in?`)) %>%
  ungroup()
  
  

final <- read_csv("E:/PD 2020 Wk 2 Input - Time Inputs.csv", col_types = 
                    cols(Date = col_date(format = "%m/%d/%y"), 
                         Time = col_character())) %>%
  mutate('Temp' = str_remove(`Time`,'\\W'),
         'Time' =  paste0(str_pad(as.integer(str_extract(`Temp`,'(\\d+)(?=\\d{2})'))
                                  +if_else(str_detect(`Temp`,'(p|P)'),12,0),
                                  2,'left','0'),
                          ':',
                          str_extract(`Temp`,'(\\d{2})(?=\\D|$)')),
         'Date Time' = as.POSIXct(paste0(format(`Date`,'%Y/%m/%d'),' ',`Time`), format = "%Y/%m/%d %H:%M")) %>%
  select(-'Temp')

View(final)