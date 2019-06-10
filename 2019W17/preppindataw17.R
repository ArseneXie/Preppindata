library(dplyr)
library(tidyr)
library(readr)

vote <- read_delim("E:/Voting Systems.csv", 
                    "\t", escape_double = FALSE, trim_ws = TRUE)

fptp <- vote %>%
  mutate('Rank1'=sapply(strsplit(`Voting Preferences`, ''), function(x) x[[1]][1])) %>%
  mutate('winner' = names(which.max(table(`Rank1`)))) %>%
  select('winner') %>%
  distinct() %>%
  mutate('Vote System' = 'fptp') 

borda_count <- vote %>%
  mutate('Rank1'=sapply(strsplit(`Voting Preferences`, ''), function(x) x[[1]][1])) %>%
  mutate('Rank2'=sapply(strsplit(`Voting Preferences`, ''), function(x) x[[2]][1])) %>%
  mutate('Rank3'=sapply(strsplit(`Voting Preferences`, ''), function(x) x[[3]][1])) %>%
  gather(., key='ranking', value='candidate', -c(`Voting Preferences`,`Voter`)) %>%
  mutate('Point'=case_when(`ranking`=='Rank1' ~ 3, `ranking`=='Rank2' ~ 2, TRUE ~ 1)) %>%
  group_by(`candidate`) %>%
  summarise('Point'=sum(`Point`)) %>%
  filter(`Point` == max(`Point`)) %>%
  mutate('winner'= `candidate`) %>%
  select('winner') %>%
  mutate('Vote System' = 'borda count') 

avtemp <- vote
avrule <- function(x) {
  avtemp <<- avtemp %>% 
    mutate('Voting Preferences'=sub(x,'',`Voting Preferences`),
           '50%Level'=n()/2) %>%
    mutate('Rank1'=sapply(strsplit(`Voting Preferences`, ''), function(x) x[[1]][1]))

  avmax <- avtemp %>%
    group_by(`Rank1`) %>%
    summarise('Count'=n(),'50%Level'=first(`50%Level`)) %>%
    filter(`Count`> `50%Level`) %>%
    select('Rank1') %>%
    rename('winner' = 'Rank1')
  
  if(nrow(avmax)==0){
    avrule(unlist(avtemp %>%
                    mutate('minvote' = names(which.min(table(`Rank1`)))) %>%
                    select('minvote') %>%
                    distinct())[[1]])
  } else {
    return(avmax)
  }
}

av <- avrule('') %>%
  mutate('Vote System' = 'av') 
  
final <- do.call('rbind', list(fptp, borda_count, av)) %>%
  select(c('Vote System','winner'))

View(final)
