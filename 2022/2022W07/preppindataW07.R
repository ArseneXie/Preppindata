library(readxl)
library(dplyr)
library(tidyr)
library(stringr)
library(lubridate)
library(purrr)

Sys.setlocale("LC_ALL","English")
people_xlsx <- "C:/Data/PreppinData/PeopleData.xlsx"
data_xlsx <- "C:/Data/PreppinData/MetricData2021.xlsx"

correct_cols <- c('id'='AgentID', 'Calls Offered'='Offered', 'Calls Not Answered'='Not Answered', 'Calls Answered'='Answered')

call_data <- data_xlsx %>%
  excel_sheets() %>%
  set_names() %>%
  map_df(
    ~ read_excel(path = data_xlsx, sheet = .x,) %>% rename(any_of(correct_cols)),
    .id = 'Month') %>%
  mutate('Month Start Date' = as.Date(paste0('2021-',`Month`,'-01'), format='%Y-%b-%d'))

final <- read_excel(people_xlsx, 'People') %>%
  mutate('Agent Name' = paste(`last_name`, `first_name`, sep=', ')) %>%
  merge(read_excel(people_xlsx, 'Location'), by = 'Location ID') %>%
  merge(read_excel(people_xlsx, 'Leaders') %>%
          mutate('Leader Name' = paste(`last_name`, `first_name`, sep=', '),
                 'Leader 1' = `id`) %>%
          select(c('Leader 1', 'Leader Name')), by='Leader 1') %>%
  crossing(., read_excel(people_xlsx, 'Date Dim') %>% filter(year(`Month Start Date`) == 2021)) %>%
  crossing(., read_excel(people_xlsx, 'Goals') %>%
             mutate('value' = as.numeric(str_extract(`Goals`, '(\\d+)$'))) %>%
             pivot_wider(names_from = 'Goals', values_from = 'value')) %>%
  merge(call_data, by=c('id', 'Month Start Date'), all.x=TRUE) %>%
  mutate('Not Answered Rate' = round(`Calls Not Answered`/`Calls Offered`,3),
         'Agent Avg Duration' = round(`Total Duration`/`Calls Answered`),
         'Met Not Answered Rate' = (`Not Answered Rate`*100 < `Not Answered Percent < 5`),
         'Met Sentiment Goal' = (`Sentiment` >= `Sentiment Score >= 0`)) %>%
  select(c('id', 'Agent Name', 'Leader 1', 'Leader Name', 'Month Start Date','Location', 'Calls Answered', 'Calls Not Answered', 
           'Not Answered Rate', 'Met Not Answered Rate', 'Not Answered Percent < 5', 'Calls Offered', 'Total Duration', 
           'Agent Avg Duration', 'Transfers', 'Sentiment', 'Sentiment Score >= 0', 'Met Sentiment Goal'))

View(final)
