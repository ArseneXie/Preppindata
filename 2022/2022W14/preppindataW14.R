library(readr)
library(dplyr)

final <- read_csv("C:/Data/PreppinData/Richard Osman's House of Games - Episode Guide - Players.csv") %>%
  rename('Series' = !!names(.[2]), 'Week' = !!names(.[3]), 'Fri Score' = !!names(.[9]), 'Score' = !!names(.[10]),
         'Fri Rank' = !!names(.[17]), 'Points' = !!names(.[22]), 'Original Rank' = !!names(.[23])) %>%
  select(c('Series', 'Week', 'Player', 'Original Rank', 'Score', 'Points', 'Fri Score', 'Fri Rank')) %>%
  filter(!is.na(`Series`) & !grepl('^N', `Series`)) %>%
  mutate('Original Rank' = as.integer(gsub('\\D', '', `Original Rank`)),
         'Fri Rank' = as.integer(gsub('\\D', '', `Fri Rank`)),
         'Points without double points Friday' = `Points` - (5-`Fri Rank`), 
         'Score if double score Friday' = `Score` + `Fri Score`) %>%
  group_by(`Week`, `Series`) %>%
  mutate('Rank without double points Friday' = rank(desc(`Points without double points Friday`), ties.method='min'),
         'Rank based on Score' = rank(desc(`Score`), ties.method='min'),
         'Rank if Double Score Friday' = rank(desc(`Score if double score Friday`), ties.method='min'),
         'Change in winner with no double points Friday?' = max((`Original Rank`==1) & (`Rank without double points Friday`!=1))>0,
         'Change in winner based on Score?' = max((`Original Rank`==1) & (`Rank based on Score`!=1))>0,
         'Change in winner if Double Score Friday?' = max((`Original Rank`==1) & (`Rank if Double Score Friday`!=1))>0) %>%
  select(c('Series', 'Week', 'Player', 'Original Rank',
           'Rank without double points Friday', 'Change in winner with no double points Friday?',
           'Rank based on Score', 'Change in winner based on Score?',
           'Rank if Double Score Friday', 'Change in winner if Double Score Friday?',
           'Points', 'Score', 'Points without double points Friday', 'Score if double score Friday')) %>%
  arrange(`Week`, `Series`, `Original Rank`)

View(final)
