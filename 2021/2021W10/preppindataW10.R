library(readxl)
library(dplyr)
library(stringr)
library(data.tree) 

xlsx <- "F:/Data/Pokemon Input.xlsx"
  
pokemon <- read_excel(xlsx, sheet = "Pokemon") %>%
  filter(!str_detect(`Name`,'^Mega\\s')) %>%
  filter(as.numeric(str_trim(`#`))<=386) %>%
  select(-'Type') %>%
  distinct()

evolution <- read_excel(xlsx, sheet = "Evolution") %>%
  distinct() %>%
  filter(`Evolving to` %in% pokemon$Name) 

rule <- evolution %>%
  select(c('Evolving from', 'Evolving to')) %>%
  filter(!(`Evolving from` %in% evolution$`Evolving to`)) %>%
  mutate('Evolving to'=`Evolving from`,
         'Evolving from'="root2") %>%
  rbind(evolution %>%
          select(c('Evolving from', 'Evolving to')) ,.) %>%
  FromDataFrameNetwork(.)

evo_grp <- ToDataFrameTree(rule, 
                           Name =  function(x) x$path[x$level],
                           `Evolution Group` = function(x) x$path[2])[-1,-1]

final <- merge(pokemon,evolution, by.x='Name', by.y='Evolving from', all.x=TRUE) %>%
  merge(., evolution %>% select(c('Evolving from', 'Evolving to')), by.x='Name', by.y='Evolving to', all.x=TRUE) %>%
  merge(., evo_grp, by='Name', all.x=TRUE) %>%
  mutate('Evolution Group' = coalesce(`Evolution Group`,`Name`)) %>%
  select(c('Evolution Group', '#', 'Name', 'Total', 'HP', 'Attack', 'Defense', 'Special Attack', 
           'Special Defense', 'Speed', 'Evolving from', 'Evolving to', 'Level', 'Condition', 'Evolution Type'))

View(final)

#---
#rule_tree<- ToDataFrameTree(rule, 
#                            level1 = function(x) x$path[2],
#                            level2 = function(x) x$path[3],
#                            level3 = function(x) x$path[4],
#                            level_number = function(x) x$level - 1)[-1,-1]
#---
