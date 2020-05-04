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
  map(~.x) %>%
  discard(~all(is.na(.x))) %>%
  map_df(~.x) 

final <- data %>%
  select(matches('^(Match Details No|Start|Subst)')) %>%
  pivot_longer(.,cols=matches('^S'),names_to = 'Type Number',values_to = 'Player Name') %>%
  mutate('Start Appearance' = ifelse(grepl('^Start',`Type Number`),1,0),
         'Player No' = str_extract(`Type Number`,'(\\d+)$')) %>%
  merge(.,data %>%
          select(matches('^(Match Details No|sub\\d)')) %>%
          pivot_longer(.,cols=matches('^s'),names_to = 'Type',values_to = 'Value') %>%
          mutate('subX' = str_extract(`Type`,'^(sub\\d)'),
                 'ValueType' = ifelse(grepl('\\.[12]$',`Type`),ifelse(grepl('\\.[1]$',`Type`),'SubOn','SubMins'),'SubOff')) %>%
          pivot_wider(.,id_cols=c('Match Details No.','subX'),names_from = 'ValueType', values_from = 'Value') %>%
          pivot_longer(.,cols=matches('Sub(On|Off)'),names_to = 'OnOff',values_to = 'Player No') %>%
          mutate('Mins Played' = ifelse(`OnOff`=='SubOff',`SubMins`,game_time-`SubMins`)),
        by=c('Match Details No.','Player No'), all.x = TRUE) %>%
  mutate('Appearances' = ifelse(is.na(`OnOff`),`Start Appearance`,1),
         'Mins Played' = ifelse(is.na(`Mins Played`),`Start Appearance`*game_time,`Mins Played`)) %>%
  group_by(`Player Name`) %>%
  summarise('In Squad' = n_distinct(`Match Details No.`),
            'Appearances' = sum(`Appearances`),
            'Mins Played' = sum(`Mins Played`),
            'Mins per Game' = ifelse(`Appearances`==0,0,`Mins Played`/`Appearances`))

View(final)