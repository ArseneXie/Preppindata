library(dplyr)
library(tidyr)
library(readxl)
library(splitstackshape)
library(stringr)
library(fuzzyjoin)
library(lubridate)

xlsx <- "F:/Data/2020W48 Input.xlsx"

flight <- read_excel(xlsx, sheet = "Stands") %>%
  cSplit(., 'Accessed by Gates', ',') %>%
  pivot_longer(.,cols=starts_with('Accessed by Gates'), names_to=NULL, values_to='Gate', values_drop_na=TRUE) %>%
  merge(read_excel(xlsx, sheet = "Remote Stands Accesibility"), by='Gate') %>%
  group_by(`Stand`) %>%
  mutate('One Gate' = if_else(n()==1,'Y','N'),
         'Stand' = as.integer(str_extract(`Stand`,'\\d+')),
         'Gate' = as.integer(str_extract(`Gate`,'\\d+'))) %>%
  merge(read_excel(xlsx, sheet = "Stand Allocations 01.02.2020 AM"), by='Stand') %>%
  mutate('Date Begin' = as.POSIXct(paste('2020-02-01',`Time`),format='%Y-%m-%d %H%M', tz='UTC'),
         'Date End' =   `Date Begin` %m+% minutes(45),
         'Time Factor' = if_else(`Requires Bus?`=='Y',-1,1)*`Time to Reach Remote Stands`) %>%  
  arrange(., desc(`One Gate`), desc(`Requires Bus?`), desc(`Time Factor`), `Flight`) %>%
  select(-c('One Gate','Time','Time Factor'))

allc_cols <- c('Flight','Stand','Requires Bus?','Time to Reach Remote Stands') 
gateall <- read_excel(xlsx, sheet = "Gate Availability") %>%
  cbind(setNames(lapply(allc_cols, function(x) x=NA), allc_cols))

allocated <- NULL
for (row in 1:nrow(flight)) {
  if(flight[row, 'Flight'] %in% allocated) {
    next
  }
  aval <- gateall %>% filter(is.na(`Flight`) & `Gate`==flight[row, 'Gate'] &
                               `Date`>=flight[row, 'Date Begin'] & `Date`<flight[row, 'Date End'] ) %>% nrow(.)
  if(aval==3){
    gateall <- fuzzy_left_join(gateall, flight[row, ],
                               by = c('Gate','Date'='Date Begin','Date'='Date End'), match_fun = list(`==`,`>=`,`<`)) %>%
      mutate('Gate'=coalesce(`Gate.x`,`Gate.y`),
             'Flight' = coalesce(`Flight.x`, `Flight.y`),
             'Stand' = coalesce(`Stand.x`, `Stand.y`),
             'Requires Bus?' = coalesce(`Requires Bus?.x`, `Requires Bus?.y`),
             'Time to Reach Remote Stands' = coalesce(`Time to Reach Remote Stands.x`, `Time to Reach Remote Stands.y`)) %>%
      select(-matches('\\.x$|\\.y$|Date Begin|Date End'))
    
    allocated <- c(allocated, flight[row, 'Flight'])
  }else{
    next
  }
} 

final <- gateall %>%
  mutate('Time to Reach Stand' = if_else(`Requires Bus?`=='N',0,`Time to Reach Remote Stands`)) %>%
  select(c('Gate', 'Stand', 'Date', 'Flight', 'Requires Bus?', 'Time to Reach Stand'))

View(final)
