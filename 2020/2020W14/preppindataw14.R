library(dplyr)
library(tidyr)
library(readr)
library(scales)

final <- read_csv("E:/PD Week 14 Input.csv", 
                  col_types = cols(Fang_length = col_number(), 
                                   Prosoma_height = col_number(), Prosoma_length = col_number(), 
                                   Prosoma_width = col_number(), Tibia_I_length = col_number(), 
                                   Total_body_length = col_number())) %>%
  drop_na() %>%
  group_by(`Species`) %>%
  filter(n()>=10) %>%
  pivot_longer(., cols=contains('_'), names_to='Trait', values_to='Value') %>%
  group_by(`Species`,`Trait`) %>%
  summarise('Value' = mean(`Value`)) %>%
  group_by(`Trait`) %>%
  mutate('Max Value' = max(`Value`),
         'Min Value' = min(`Value`),
         'Normalised Value' = (`Value`-`Min Value`)/(`Max Value`-`Min Value`)) %>%
  ungroup() %>% 
  mutate('Species' = gsub('_',' ',`Species`),
         'Trait' = gsub('_',' ',`Trait`)) 

# Alternative method: Calculate with scales::rescale
final <- final %>%
  group_by(`Trait`) %>%
  mutate('Normalised Value Alt' = rescale(`Value`, to=c(0,1)))

View(final)