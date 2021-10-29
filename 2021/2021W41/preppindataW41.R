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
  group_by() %>%
  

NA_character_
?case_when

test <- str_extract('	SOUTH-2','(\\d)')

names(final)[length(names(final))-1]<-"space" 

substr('2012-13',1,4)

  rename('Pts' = !!names(.[2]))
  `Date`-lag(`Date`)

  
  rename('Cocktails' = !!names(.[1]),
         'Ingredient' = !!names(.[2]),
         'Cocktail Price' = !!names(.[3]))

final <- read_table2("C:/Data/PreppinData/Southend Stats.csv") 


test <- Southend_Stats <- read_delim("C:/Data/PreppinData/Southend Stats.csv", 
                                     delim = "\\s", escape_double = FALSE, 
                                     trim_ws = TRUE)

%>%
  mutate('Datetime' = as.POSIXct(paste(`Date`, `Time`),format='%d/%m/%Y %H:%M:%S'),
         'Bike Type' = if_else(`Data Parameter`=='Bike Type', `Data Value`, NA_character_),
         'Batch Status' = if_else(`Data Parameter`=='Batch Status', `Data Value`, NA_character_),
         'Name of Process Stage' = if_else(`Data Parameter`=='Name of Process Stage', `Data Value`, NA_character_)) %>%
  group_by(`Batch No.`) %>%
  arrange(`Datetime`) %>%
  fill(`Bike Type`, `Batch Status`, `Name of Process Stage`) %>%
  filter((`Data Type`=='Process Data') & (`Data Parameter`!='Name of Process Stage')) %>%
  mutate('Actual' = if_else(str_detect(`Data Parameter`, '^(Actual)'), as.numeric(`Data Value`), NA_real_),
         'Target' = if_else(str_detect(`Data Parameter`, '^(Target)'), as.numeric(`Data Value`), NA_real_),
         'Data Parameter' = str_remove(`Data Parameter`,'^(\\w+\\s)')) %>%
  select(c('Batch No.', 'Bike Type', 'Batch Status', 'Name of Process Stage',
           'Data Parameter', 'Actual', 'Target', 'Datetime'))

View(final)

?read_table2

?read_fwf

?read_csv