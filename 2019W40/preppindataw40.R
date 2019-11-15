library(dplyr)
library(tidyr)
library(readxl)
library(stringr)
library(splitstackshape)

food_rate <- c('Horrendous' = 1,'Just about edible but I was hungry' = 2,'Some good, some not so good' =3,
               'Yum!' = 4,'Give the team a Michelin star!!' = 5)
get_food_rate <- function(x) { food_rate[x] }

resp <- read_excel(path = "E:/Sudzilla Conference feedback (Responses).xlsx", 
                   sheet = "Form responses 1")
nps <- resp %>%
  summarise('Total Respondents' = n(),
            'Promoter' = sum(`On a scale of 0-10, how would you rate Sudzilla?`>=9),
            'Detractor' = sum(`On a scale of 0-10, how would you rate Sudzilla?`<=6),
            'NPS Score' = round((`Promoter`-`Detractor`)/`Total Respondents`*100,1))

detail <- resp %>%
  mutate('Food Rating Score' = rowMeans(select(.,contains('rate the food')) %>% mapply(get_food_rate,.), na.rm = TRUE),
         'Keynote Rating Score'=rowMeans(select(.,ends_with('keynote?')), na.rm = TRUE)) %>%
  select(-contains('rate the food')) %>%
  select(-ends_with('keynote?')) %>%
  cSplit(.,'Which three words would you use describe to Sudzilla? (separate with a comma)',',') %>%
  gather(., key='ToDrop', value='Which three words would you use describe to Sudzilla? (separate with a comma)',
         starts_with('Which three words'),na.rm=TRUE) %>%
  mutate('Which three words would you use describe to Sudzilla? (separate with a comma)'=
           str_replace(`Which three words would you use describe to Sudzilla? (separate with a comma)`,'\\W+$','')) %>%
  select(-'ToDrop') 
  
View(nps)
View(detail)