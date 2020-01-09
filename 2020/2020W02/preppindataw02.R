library(dplyr)
library(readr)
library(stringr)

final <- read_csv("E:/PD 2020 Wk 2 Input - Time Inputs.csv", col_types = 
                    cols(Date = col_date(format = "%m/%d/%y"), 
                         Time = col_character())) %>%
  mutate('Temp' = str_remove(`Time`,'\\s|\\W'),
         'Time' =  paste0(str_pad(as.integer(str_extract(`Temp`,'(\\d+)(?=\\d{2})'))
                                  +if_else(str_detect(`Temp`,'(p|P)'),12,0),
                                  2,'left','0'),
                          ':',
                          str_extract(`Temp`,'(\\d{2})(?=\\D|$)')),
         'Date Time' = as.POSIXct(paste0(format(`Date`,'%Y/%m/%d'),' ',`Time`), format = "%Y/%m/%d %H:%M")) %>%
  select(-'Temp')

View(final)