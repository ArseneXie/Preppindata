library(dplyr)
library(readxl)

xlsx <- "F:/Data/Roman Numerals.xlsx"

final <- read_excel(xlsx, sheet = "Number") %>%
  mutate('Numeric Equivalent' = as.numeric(as.roman(`Number`)))

View(final)