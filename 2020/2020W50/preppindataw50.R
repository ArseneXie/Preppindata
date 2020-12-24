library(readxl)
library(dplyr)
library(stringr)

final <- read_excel( "F:/Data/Secret Santa.xlsx") %>%
  arrange(.,`Secret Santa`) %>%
  mutate('Secret Santee' = lead(`Secret Santa`,default = min(`Secret Santa`)),
         'Email' = str_replace_all(`Email`, '(.*)@([a-z]+).([a-z]+)','\\1@\\2.\\3'),
         'Email Subject' = 'Secret Santa????????',
         'Email Body' = paste0(`Secret Santa`,', the results are in, your secret santee is: ',`Secret Santee`,'. Good luck finding a great gift!')) %>%
  select(c('Email', 'Email Subject', 'Email Body'))

View(final)
