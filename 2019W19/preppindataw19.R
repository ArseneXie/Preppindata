library(readxl)
library(dplyr)

record <- read_excel("E:/2018 Tour de France times.xlsx")

get_sec<- function(x) {
  timepart <- as.numeric(unlist(regmatches(x, gregexpr("[[:digit:]]+", x)))) 
  timepart <- rev(timepart)*c(1,60,60*60)
  return(sum(timepart))
}

final <- record %>%
  rowwise() %>% 
  mutate('Gap in Sec' = get_sec(`Gap`)) %>%
  ungroup() %>%
  group_by(`Team`) %>%
  summarise('Number of Riders'=n(),'Team Avg Gap in Sec'=mean(`Gap in Sec`)) %>%
  filter(`Number of Riders`>=7 & `Team Avg Gap in Sec`<=60*100) %>%
  mutate('Team Avg Gap in Min' = as.integer(`Team Avg Gap in Sec`/60)) %>%
  select(-'Team Avg Gap in Sec')

View(final)
