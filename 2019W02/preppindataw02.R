library(readxl)
library(dplyr)
library(tidyr)

final <- read_excel("E:/Week Two Input.xlsx", 
                    col_types = c("text", "text", "text", 
                                  "numeric", "date")) %>%
  drop_na() %>%
  mutate('City' = if_else(grepl('.*gh$',`City`),'Edinburgh','London')) %>%
  unite('R2CHdr',`Metric`,`Measure`, sep=' - ') %>%
  spread(`R2CHdr`,`Value`)

View(final)
