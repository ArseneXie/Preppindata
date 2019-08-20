library(readxl)
library(dplyr)

sales <- read_excel("E:/PD - Week 27.xlsx", 
                    col_types = c("text", "date", "numeric")) %>%
  mutate('Pre/Post Valentines Day' = if_else(as.Date(`Date`)<= as.Date('2019-02-14'),'Pre','Post')) %>%
  group_by(`Pre/Post Valentines Day`,`Store`) %>%
  arrange(`Date`) %>%
  mutate('Running Total Sales' = cumsum(`Value`)) %>%
  rename('Daily Store Sales' = 'Value')

View(sales)




library(ggplot2)
rowdata <- sales %>%
  mutate('Pre-Post'=factor(`Pre/Post Valentines Day`, levels=c('Pre','Post')))
p <- ggplot(rowdata, aes(x=`Date`)) +
  geom_line(aes(y = `Daily Store Sales`), colour = 'Blue') +
  geom_line(aes(y = `Running Total Sales`*900/5000), colour = 'Red')

q <- p + facet_grid(`Store` ~ `Pre-Post`, scales='free')

q
            
