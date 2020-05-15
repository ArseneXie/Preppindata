library(dplyr)
library(readxl)
library(tidyr)
library(stringr)
library(purrr)

xlsx <- 'E:/Liverpool Lineups.xlsx'
game_time <- 90
data_head <- read_excel(xlsx, col_names = FALSE, skip = 4, n_max = 4) %>%
  mutate('col_level' = row_number()) %>%
  filter(`col_level`<=2) %>%
  gather(., key='var', value='cols', -'col_level') %>%
  group_by(`col_level`) %>% 
  fill(`cols`) %>%
  spread(.,`col_level`, `cols`) %>%
  mutate('col_name' = ifelse(grepl('^sub',`2`),`2`,paste(`1`,`2`))) %>%
  arrange(as.integer(str_extract(`var`,'\\d+'))) %>% 
  group_by(`col_name`) %>% 
  mutate('Indicator' = cumsum(ifelse(`col_name`==lag(`col_name`, default='#'),1,0))) %>%
  mutate('fin_col_name' = ifelse(`Indicator`==0,`col_name`,paste0(`col_name`,'.',`Indicator`)))
data <- read_excel(xlsx, skip = 7 ,col_names = FALSE) %>%
  rename_all(funs(data_head[['fin_col_name']][as.integer(str_extract(.,'\\d+'))])) %>%
  map(~.x) %>% discard(~all(is.na(.x))) %>% map_df(~.x) 

opt1 <- data %>%
  select(c('Match Details Location','Match Details Result', 'Match Details Formation','Match Details Oppo Form.')) %>%
  separate(`Match Details Result`,c('GoalsA','GoalsB'), sep='-') %>%
  mutate('Liverpool Goals' = as.numeric(if_else(`Match Details Location`=='H',`GoalsA`,`GoalsB`)),
         'Opposition Goals' = as.numeric(if_else(`Match Details Location`=='A',`GoalsA`,`GoalsB`))) %>%
  rename('Formation' = 'Match Details Formation', 'Oppo Form.' = 'Match Details Oppo Form.') %>%
  group_by(`Formation`,`Oppo Form.`)%>%
  summarise('Games Played' = n(),
            'Avg Goals Scored' = mean(`Liverpool Goals`),
            'Liverpool Goals' = sum(`Liverpool Goals`),
            'Avg Goals Conceded' = mean(`Opposition Goals`),
            'Opposition Goals' = sum(`Opposition Goals`)) %>%
  select(c('Formation', 'Oppo Form.', 'Games Played', 'Liverpool Goals','Avg Goals Scored', 'Opposition Goals', 'Avg Goals Conceded'))

opt2 <- data %>%
  select(matches('^(Match Details No|Match Details Formation|Start|Subst)')) %>%
  pivot_longer(.,cols=matches('^S'),names_to = 'Type Number',values_to = 'Player Name') %>%
  mutate('Start Appearance' = ifelse(grepl('^Start',`Type Number`),1,0),
         'Player No' = str_extract(`Type Number`,'(\\d+)$')) %>%
  merge(.,data %>%
          select(matches('^(Match Details No|sub\\d)')) %>%
          pivot_longer(.,cols=matches('^s'),names_to = 'Type',values_to = 'Value') %>%
          mutate('subX' = str_extract(`Type`,'^(sub\\d)'),
                 'ValueType' = ifelse(grepl('\\.[12]$',`Type`),ifelse(grepl('\\.[1]$',`Type`),'SubOn','SubMins'),'SubOff')) %>%
          group_by(`Match Details No.`,`subX`) %>%
          mutate('SubOff Position' = sum(if_else(`ValueType`=='SubOff',`Value`,0))) %>%
          pivot_wider(.,id_cols=c('Match Details No.','subX','SubOff Position'),names_from = 'ValueType', values_from = 'Value') %>%
          pivot_longer(.,cols=matches('Sub(On|Off)$'),names_to = 'OnOff',values_to = 'Player No') %>%
          mutate('Mins Played' = ifelse(`OnOff`=='SubOff',`SubMins`,game_time-`SubMins`)),
        by=c('Match Details No.','Player No'), all.x = TRUE) %>%
  mutate('Appearances' = ifelse(is.na(`OnOff`),`Start Appearance`,1),
         'Mins Played' = ifelse(is.na(`Mins Played`),`Start Appearance`*game_time,`Mins Played`),
         'Last Name' = tolower(`Player Name`)) %>% select(-'Player Name') %>%
  merge(.,read_excel('E:/PlayerList.xlsx') %>%
          mutate('Preferred Position' = str_extract(`Player Name`,'([A-Z])(?=\\))'),
                 'Player Name' = str_trim(str_extract(`Player Name`,'(\\D+)(?=\\()')),
                 'Last Name' = tolower(str_remove(`Player Name`,'^\\S+\\s'))),
        by='Last Name') %>%
  mutate('Player Position' = if_else(is.na(`SubOff Position`),as.integer(`Player No`),as.integer(`SubOff Position`))) %>%
  merge(.,read_excel('E:/Formation Positions.xlsx'),
        by.x=c('Player Position','Match Details Formation'), by.y=c('Player Position','Formation Name')) %>%
  group_by(`Player Name`,`Position Type`,`Position Name`,`Preferred Position`) %>%
  summarise('No Times Played' = sum(`Appearances`),
            'Mins Played' = sum(`Mins Played`)) %>%
  filter(`No Times Played`>0) %>%
  group_by(`Player Name`) %>%
  mutate('Games Oop' = sum(if_else(substring(`Position Type`,1,1)==`Preferred Position`,0,`No Times Played`))) %>%select(-'Preferred Position')

View(opt1)
View(opt2)