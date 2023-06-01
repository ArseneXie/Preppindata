library(dplyr)
library(readr)

final <- read_csv("C:/Data/PreppinData/Transactions.csv") %>%
  merge(read_csv("C:/Data/PreppinData/Swift Codes.csv"), by='Bank') %>%
  mutate('Sort Code' = gsub('-','',`Sort Code`),
         'IBAN' = paste0('GB', `Check Digits`, `SWIFT code`, `Sort Code`, `Account Number`)) %>%
  select(c('Transaction ID', 'IBAN'))
  
View(final)