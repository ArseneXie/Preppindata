library(readxl)
library(dplyr)
library(tidyr)
library(stringr)
library(openxlsx)

xlsx <- "F:/Data/Week 14 - Input.xlsx"

position <- function(k){
  return(if_else(k == 'A'| k=='F','Window',if_else(k == 'B'| k=='E','Middle','Aisle')))
}

df <- read_excel(xlsx, sheet = 'FlightDetails') %>% 
  rename('infostr' = !!names(.[1])) %>%
  mutate('FlightNo.' = as.integer(str_extract(`infostr`,'(?<=\\[)(\\d+)')),
         'Depart Hour' = as.integer(str_extract(`infostr`,'(?<=\\|)(\\d+)(?=:)')),
         'Depart Time of Day' = if_else(`Depart Hour`<12,'Morning',if_else(`Depart Hour`>18,'Evening','Afternoon'))) %>%
  merge(., read_excel(xlsx, sheet = 'PlaneDetails') %>%
          mutate('RowRule' = as.integer(str_extract(`Business Class`,'(\\d+)$'))), by='FlightNo.') %>%
  select(c('FlightNo.', 'RowRule', 'Depart Time of Day')) %>%
  merge(., read_excel(xlsx, sheet = 'Passenger List') %>%
          select(c('flight_number', 'passenger_number', 'purchase_amount')), by.x='FlightNo.', by.y='flight_number') %>%
  merge(., read_excel(xlsx, sheet = 'SeatList') %>%
          pivot_longer(cols=-'Row', names_to='Seat Position', values_to='passenger_number', 
                       names_transform = list(`Seat Position` = position)), by='passenger_number') %>%
  mutate('Business Class' = if_else(`Row`>`RowRule`,'Economy','Business Class'),
         'Amount' = if_else(`Row`>`RowRule`,`purchase_amount`,0))
  
finA <- df %>%
  group_by(`Depart Time of Day`) %>%
  summarise('Avg per Flight' = sum(`Amount`)/n_distinct(`FlightNo.`), .groups = 'drop') %>%
  mutate('Rank' = rank(desc(`Avg per Flight`))) %>%
  select(c('Rank', 'Depart Time of Day', 'Avg per Flight')) %>%
  arrange(`Rank`)

finB <- df %>%
  group_by(`Seat Position`) %>%
  summarise('Purchase Amount' = sum(`Amount`), .groups = 'drop') %>%
  mutate('Rank' = rank(desc(`Purchase Amount`))) %>%
  select(c('Rank', 'Seat Position', 'Purchase Amount')) %>%
  arrange(`Rank`)

finC <- df %>%
  group_by(`Business Class`) %>%
  summarise('Purchase Amount' = sum(`purchase_amount`), .groups = 'drop') %>%
  mutate('Rank' = rank(desc(`Purchase Amount`))) %>%
  select(c('Rank', 'Business Class', 'Purchase Amount')) %>%
  arrange(`Rank`)

fin_sheet <- list("Time of day" = finA, "Seat position" = finB, "Business or Economy" = finC)
write.xlsx(fin_sheet, file = "F:/Data/prepindata2021w14r.xlsx")
