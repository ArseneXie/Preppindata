library(readxl)
library(dplyr)
library(tidyr)
library(stringr)


finalA <- read_excel("F:/Data/USOpenWinners.xlsx") %>%
  rename_all(str_to_title) %>%
  pivot_longer(., col=starts_with('Round'), names_to='Round Num', values_to='Round Score') %>%
  mutate('Round Par' = round((`Total`- as.integer(ifelse(`To Par`=='E',0,`To Par`)))/4),
         'Round to Par' = `Round Score` - `Round Par`,
         'Round Colors' = case_when(`Round Num`=='Round 1'~'A', `Round Num`=='Round 2'~'B', `Round Num`=='Round 3'~'C', TRUE ~ 'D'),
         'Point1' = case_when(`Round Num`=='Round 1'~'1,0', `Round Num`=='Round 2'~'1,-1', `Round Num`=='Round 3'~'0,-1', TRUE ~ '0,0'),
         'Point2' = case_when(`Round Num`=='Round 1'~'0,0', `Round Num`=='Round 2'~'0,-1', `Round Num`=='Round 3'~'-1,-1', TRUE ~ '-1,0'),
         'Point3' = case_when(`Round Num`=='Round 1'~'0,1', `Round Num`=='Round 2'~'0,0', `Round Num`=='Round 3'~'-1,0', TRUE ~ '-1,1'),
         'Point4' = case_when(`Round Num`=='Round 1'~'1,1', `Round Num`=='Round 2'~'1,0', `Round Num`=='Round 3'~'0,0', TRUE ~ '0,1')) %>%
  pivot_longer(., col=starts_with('Point'), names_to='Point', values_to='Coordinate') %>%
  merge(.,read_excel("F:/Data/Location Prize Money.xlsx") %>% select(c('Year', 'Country', 'Venue', 'Location')), by='Year') %>%
  separate(`Coordinate`, c('X Coordinate Polygon', 'Y Coordinate Polygon'), sep =',', convert = TRUE) %>%
  mutate('X Coordinate Polygon' = `X Coordinate Polygon`*sqrt(`Round Score`),
         'Y Coordinate Polygon' = `X Coordinate Polygon`*sqrt(`Round Score`),
         'Decade' = as.integer(`Year`/10)*10,
         'Row' = as.integer((`Decade` - min(`Decade`))/10+1),
         'Column' = `Year` - `Decade` + 1) %>%
  select(-c('Pos', 'To Par'))


finalB <- finalA %>%
  group_by(`Decade`) %>%
  summarise('Min Round Score' = min(`Round Score`),
            'Max Round Score' = max(`Round Score`),
            'Min Total Score' = min(`Total`),
            'Max Total Score' = max(`Total`), .groups='drop')

View(finalA)
View(finalB)
