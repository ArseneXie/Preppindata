library(magrittr)
library(readxl)

xlsx <- "F:/Data/PD 2021 Wk 27 Input.xlsx"

seeding <- read_excel(xlsx, sheet = 'Seeding') %>%
  `colnames<-`(c('Seed', paste0('Round',c(1:14)))) %>%
  merge(., read_excel(xlsx, sheet = 'Teams'), by='Seed') 

picked <- data.frame(`Actual Pick`=numeric(), Seed=numeric(), Team=character())

for(i in 1:4) {
  df <- sample_n(seeding %>% select(c('Seed', 'Team')), size=1, weight=seeding[[paste0('Round',i)]]) %>%
    mutate('Actual Pick' = i)
  seeding %<>% filter(`Seed` != df[['Seed']])
  picked <- rbind(picked, df)
}

final <- rbind(picked, seeding %>% 
                 select(c('Seed', 'Team')) %>%
                 mutate('Actual Pick' = rank(`Seed`) +i)) %>%
  rename('Original' = 'Seed') %>%
  select(c('Actual Pick', 'Original', 'Team'))

View(final)
