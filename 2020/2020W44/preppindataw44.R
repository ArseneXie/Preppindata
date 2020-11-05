library(dplyr)
library(tidyr)
library(readxl)

extract_data <- function(gender, sk, nr){
  
  path <- paste0("F:/Data/2019",tolower(gender),"names.xlsx")
  data_head <- read_excel(path, col_names = FALSE, skip = sk-1, n_max = 3) %>%
    select_if(function(x) any(!is.na(x))) %>%
    mutate('col_level' = row_number()) %>%
    gather(., key='var', value='cols', -'col_level') %>%
    group_by(`col_level`) %>% 
    fill(`cols`) %>%
    spread(.,`col_level`, `cols`) %>%
    mutate('col_name' = ifelse(is.na(`2`),`1`,paste0(`1`,'-',`2`))) %>%
    arrange(as.integer(str_extract(`var`,'\\d+')))
  
  df <- read_excel(path, skip = sk+2, n_max = nr, col_names=FALSE) %>%
    select_if(function(x) any(!is.na(x))) %>%
    `colnames<-`(data_head[['col_name']]) %>%
    pivot_longer(.,cols=ends_with('Rank'), names_to='Type1', values_to='Rank' ,values_drop_na=TRUE) %>%
    pivot_longer(.,cols=ends_with('Name'), names_to='Type2', values_to='Name' ,values_drop_na=TRUE) %>%
    rowwise() %>%
    filter(strsplit(`Type1`,'-')[[1]][1]==strsplit(`Type2`,'-')[[1]][1]) %>%
    pivot_longer(.,cols=ends_with('Count'), names_to='Type3', values_to='Count' ,values_drop_na=TRUE) %>%
    rowwise() %>%
    filter(strsplit(`Type1`,'-')[[1]][1]==strsplit(`Type3`,'-')[[1]][1]) %>%
    separate(`Type1`, c('Month','Type1'),sep='-') %>%
    mutate('Gender'= gender) %>%
    select(c('Gender', 'Month', 'Rank', 'Name', 'Count')) 

  return(df)  
}

final1 <- rbind(extract_data('Boys',5,10),extract_data('Boys',19,10),extract_data('Boys',33,10),
                extract_data('Girls',5,10),extract_data('Girls',19,11),extract_data('Girls',34,12)) %>%
  arrange(`Gender`, match(`Month`, month.name))

final2 <- final1 %>%
  group_by(`Gender`,`Name`) %>%
  summarise('Count'=sum(`Count`)) %>%
  mutate('2019 Rank' = rank(desc(`Count`))) %>%
  filter(`2019 Rank`<=10) %>%
  arrange(`Gender`,`2019 Rank`) %>%
  select(c('Gender', '2019 Rank', 'Name', 'Count'))

View(final1)
View(final2)