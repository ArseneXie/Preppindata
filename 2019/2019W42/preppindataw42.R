library(dplyr)
library(tidyr)
library(readxl)
library(RJSONIO)

checklocation = function(city_name,country_name) {
  city_name_fixed = gsub(' ', '%20', city_name)
  country_name_fixed = gsub(' ', '%20', country_name)
  url = paste0(
    "http://nominatim.openstreetmap.org/search?city=",
    city_name_fixed,
    "&country=",
    country_name_fixed,
    "&limit=1&format=json")
  resOSM = fromJSON(url)
  if(length(resOSM) > 0) {
    return(1)
  } else {
    return(0) 
  }
}

Sys.setlocale("LC_ALL", "English")

final <- read_excel(path = "E:/PD Wk 42 Input.xlsx", 
                   sheet = "Sheet1") %>%
  separate(.,'Location',c('City','Country'),sep=',\\s*') %>%
  separate(.,'Store Potential Sales',c('Store Potential Sales','Currency'),sep='\\s+',convert=TRUE) %>%
  separate(.,'Store Cost',c('Store Cost','Currency'),sep='\\s+',convert=TRUE) %>%
  rename('Zip Code' = 'Potential Store Location') %>%
  filter(`Store Potential Sales` > `Store Cost`) %>%
  rowwise() %>%
  mutate('Check' = checklocation(`City`,`Country`)) %>%
  ungroup() %>%
  filter(`Check`==1) %>%
  merge(.,read_excel(path = "E:/PD Wk 42 Input.xlsx", 
                     sheet = "Currency Conversion"),
        by = 'Currency') %>%
  group_by(`Zip Code`) %>%
  filter(`Store Potential Sales`== max(`Store Potential Sales`)) %>%
  select(c('City', 'Country', 'Zip Code', 'Store Potential Sales', 'Store Cost',
           'Currency', 'Value in USD'))

View(final)