library(readxl)
library(dplyr)
library(tidyr)
library(lubridate)

espn <- read_excel("E:/PD - ESPN stats.xlsx", 
                   col_types = c("date", "text", "text", 
                                 "text", "text", "text", "text"))

clean_wl <- function(wl){
  sapply(wl,function(wl){
    if (grepl('.*-.*',wl)){
      return(wl)
    } else {
      td <- as.Date(as.numeric(wl),origin = "1899-12-30")
      return(paste0(as.character(day(td)),'-',as.character(month(td))))
    }  
  })
}

final <- espn %>%
  mutate('W-L' = clean_wl(`W-L`)) %>%
  gather(., key='vara', value='tempa', 'HI POINTS','HI REBOUNDS','HI ASSISTS') %>%
  separate(`tempa`,c('Player','Value')) %>%
  gather(., key='varb', value='tempb', 'Player','Value') %>%
  unite('varc', `vara`, `varb`, sep = ' - ') %>%
  spread(varc, tempb) %>%
  mutate_at(vars(matches(" - Value")),as.numeric) %>%
  mutate('True Date' = if_else(month(`DATE`)<10,`DATE`,`DATE` %m+% years(-1))) %>%
  mutate('OPPONENT(clean)' = gsub('^(@|vs)', '',`OPPONENT`)) %>%
  mutate('Win or Loss' = substr(`RESULT`, 1, 1)) %>%
  mutate('Home or Away' = if_else(grepl('^@',`OPPONENT`), 'Away', 'Home')) %>%
  select('OPPONENT(clean)','HI ASSISTS - Player','HI ASSISTS - Value','HI REBOUNDS - Player','HI REBOUNDS - Value',
         'HI POINTS - Player','HI POINTS - Value','Win or Loss','Home or Away','True Date','OPPONENT','RESULT','W-L')
   
View(final)