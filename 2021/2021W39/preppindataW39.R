library(readr)
library(dplyr)

get_floor <- function(floor_str){
  return(as.integer(if_else(floor_str=='G', '0', if_else(floor_str=='B', '-1',floor_str))))
}

final <- read_csv("F:/Data/2021W30.csv") %>%
  arrange(`Hour`,`Minute`) %>%
  mutate('From'= get_floor(`From`),
         'To'= get_floor(`To`),
         'Floors Btw Trips' = abs(lag(`To`)-`From`)) %>%
  group_by(`From`) %>%
  mutate('FromCount' = n()) %>%
  ungroup() %>%
  mutate('Default Position' = .[[max(which(`FromCount`== max(`FromCount`))),'From']],
         'From Default Position' = abs(`Default Position`-`From`)) %>%
  group_by(`Default Position`) %>%
  summarise('Avg travel from default position' = mean(`From Default Position`),
            'Avg travel between trips currently' = mean(`Floors Btw Trips`, na.rm=TRUE),
            'Difference' = `Avg travel from default position` - `Avg travel between trips currently`)

View(final)