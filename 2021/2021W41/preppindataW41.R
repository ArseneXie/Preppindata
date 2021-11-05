library(readr)
library(dplyr)
library(tidyr)
library(stringr)

final <- read_table("C:/Data/PreppinData/Southend Stats.csv") %>%
  rename('Pts' = names(.)[length(names(.))-1]) %>%
  arrange(`SEASON`) %>%
  mutate('Special Circumstances'=if_else(`SEASON`==max(`SEASON`),'Incomplete',
                                         if_else(substr(`SEASON`,1,4)=='1939','Abandoned due to WW2','N/A')),
         'POS' = if_else(`Special Circumstances`=='N/A',`POS`,NA_character_),
         'League Num' = if_else(`LEAGUE`=='FL-CH',0,
                                if_else(`LEAGUE`=='NAT-P',5, 
                                        as.double(str_extract_all(`LEAGUE`,'(\\d)')))),
         'Outcome' = if_else(`League Num` - lead(`League Num`) >0,'Promoted',
                             if_else(`League Num` - lead(`League Num`) <0,'Relegated','Same League')),
         'Year' = as.integer(substr(`SEASON`,1,4))) %>%
  complete(., `Year` = full_seq(`Year`, period = 1)) %>%
  mutate('Special Circumstances' = if_else(is.na(`SEASON`),if_else(`Year`<1939,'WW1','WW2'),`Special Circumstances`),
         'SEASON' = if_else(is.na(`SEASON`),paste(`Year`,(`Year`+1)%%100,sep='-'),`SEASON`)) %>%
  select(c('SEASON', 'Outcome', 'Special Circumstances', 'LEAGUE', 'P', 'W', 'D', 'L', 'F', 'A', 'Pts', 'POS'))

View(final)
