library(readxl)
library(dplyr)
library(tidyr)

final <- read_excel("F:/Data/PGALPGAMoney2019.xlsx", sheet = "OfficialMoney",
                    col_types = c("text", "numeric", "numeric", "text")) %>%
  mutate('Overall Rank' = rank(desc(`MONEY`))) %>%
  group_by(`TOUR`) %>%
  mutate('Tour Rank' = rank(desc(`MONEY`)),
         'Difference of Ranking' = `Overall Rank`-`Tour Rank`) %>%
  summarise('Avg Difference of Ranking' = mean(`Difference of Ranking`),
            'Avg Money per Event' = round(mean(`MONEY`/`EVENTS`)),
            'Number of Events' = sum(`EVENTS`),
            'Number of Players' = n_distinct(`PLAYER NAME`),
            'Total Prize Money' = sum(`MONEY`),
            .groups = 'drop') %>%
  pivot_longer(cols=-'TOUR', names_to='Measure', values_to ='Value') %>%
  pivot_wider(id_cols='Measure', names_from='TOUR', values_from='Value') %>%
  mutate('Difference between tours' = `LPGA`-`PGA`)

View(final)
