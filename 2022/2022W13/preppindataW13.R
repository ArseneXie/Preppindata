library(readr)
library(dplyr)

sales <- read_csv("C:/Data/PreppinData/Pareto Input.csv") %>%
  group_by(`Customer ID`, `First Name`, `Surname`) %>%
  summarise('Sales' = sum(`Sales`), .groups='drop') %>%
  arrange(desc(`Sales`)) %>%
  mutate('% of Total' = `Sales`/sum(`Sales`)*100, 
         'Running % of Total Sales' = round(cumsum(`% of Total`), 2))

gen_output <- function(sales_df, pert_of_sales){
  df1 <- sales_df %>% filter(`Running % of Total Sales` <= pert_of_sales)
  write.csv(df1, paste0('C:\\Pareto Output ',pert_of_sales,'%.csv'), row.names = FALSE)
  
  outcome<- paste0(round(nrow(df1)/nrow(sales_df)*100), '% of Customers account for ', pert_of_sales, '% of Sales')
  df2 <- data.frame(outcome)
  write.csv(df2, paste0('C:\\Pareto In Words ',pert_of_sales,'%.csv'), row.names = FALSE)
  return(df1)
}

final <- gen_output(sales, 80)

View(final)
