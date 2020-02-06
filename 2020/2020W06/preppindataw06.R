library(dplyr)
library(readxl)
library(stringr)

xlsx <- "E:/PD 2020 Wk 6 Input.xlsx"

final <- read_excel(xlsx, sheet = "GBP to USD conversion rate", col_types = c("date", "text")) %>%
  mutate('Week' = paste('wk',as.integer(strftime(`Date`,format='%U'))+1,strftime(`Date`,format='%Y')),
         'Conv Rate' = as.numeric(str_extract(`British Pound to US Dollar`,'(?<=\\s)(\\d\\.\\d+)'))) %>%
  group_by(`Week`) %>%
  summarise('Max Conv Rate' = max(`Conv Rate`),
            'Min Conv Rate' = min(`Conv Rate`)) %>%
  merge(.,read_excel(xlsx,sheet = "Sales") %>%
          mutate('Week' = paste('wk',`Week`,`Year`)), by='Week') %>%
  mutate('UK Sales Value (GBP)' = round(`Sales Value`*(1-`US Stock sold (%)`/100),2),
         'US Sales Value (GBP)' = `Sales Value`-`UK Sales Value (GBP)`,
         'US Sales (USD) Best Case' = round(`US Sales Value (GBP)`*`Max Conv Rate`,2),
         'US Sales (USD) Worst Case' = round(`US Sales Value (GBP)`*`Min Conv Rate`,2),
         'US Sales Potential Variance' = `US Sales (USD) Best Case`-`US Sales (USD) Worst Case`) %>%
  select(c('Week', 'UK Sales Value (GBP)', 'US Sales (USD) Best Case', 
           'US Sales (USD) Worst Case', 'US Sales Potential Variance'))

View(final)