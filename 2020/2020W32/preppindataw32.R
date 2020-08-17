library(dplyr)
library(readxl)
library(zoo)

final <- read_excel("F:/Data/Copy Down Data Challenge.xlsx") %>%
  do(na.locf(.))

View(final)