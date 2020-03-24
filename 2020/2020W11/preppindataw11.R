library(dplyr)
library(tidyr)
library(readxl)
library(ompr)
library(ompr.roi)
library(ROI)
library(ROI.plugin.glpk)

xlsx <- "E:/PD 2020 Week 11 Input.xlsx"

orders <- read_excel(xlsx, sheet = "Orders")
order <- pull(orders %>% arrange(`Order Number`),`Order Size`)
boxes <- pull(read_excel(xlsx, sheet = "Box Sizes") %>% arrange(`Box Size`),`Box Size`)
n <- length(order)

solution <- MILPModel() %>%
  add_variable(box_a[i], i = 1:n, lb = 0, type = "integer") %>%
  add_variable(box_b[i], i = 1:n, lb = 0, ub = boxes[3]/boxes[2]-1,type = "integer") %>%
  add_variable(box_c[i], i = 1:n, lb = 0, ub = boxes[2]/boxes[1]-1,type = "integer") %>%
  add_variable(box_d[i], i = 1:n, lb = 0, ub = boxes[1]-1,type = "integer") %>%
  set_objective(0) %>%
  add_constraint(boxes[3]*box_a[i]+boxes[2]*box_b[i]+boxes[1]*box_c[i]+box_d[i] == order[i], i = 1:n) %>%
  solve_model(with_ROI(solver = "glpk")) 

  
detail <- list(get_solution(solution,box_a[i]),
               get_solution(solution,box_b[i]),
               get_solution(solution,box_c[i]),
               get_solution(solution,box_d[i])) %>%
  do.call('rbind', .) %>%
  rename('Order Number'='i') %>%
  mutate('Box Size' = if_else(`variable`=='box_a',boxes[3],if_else(`variable`=='box_b',boxes[2],boxes[1])),
         'Box Count' = if_else(`variable`=='box_d',sign(`value`),`value`),
         'Soaps in Box' = if_else(`variable`=='box_d',`value`,`Box Size`)) %>%
  select(-c('variable','value'))

boxes_per_order <- merge(orders, detail %>% select(-'Soaps in Box'), by='Order Number') %>%
  mutate('Box Size' = paste('Boxes of',`Box Size`)) %>%
  pivot_wider(names_from = 'Box Size', values_from = 'Box Count', values_fn = list(`Box Count` = sum)) %>%
  select(c('Order Number', 'Order Size', 'Boxes of 120', 'Boxes of 24','Boxes of 6'))

df <-  merge(orders, detail %>% filter(`Box Count`>0), by='Order Number') 
soaps_per_box <- df[rep(seq(nrow(df)), df$`Box Count`),] %>%
  arrange(`Order Number`,desc(`Soaps in Box`)) %>%
  group_by(`Order Number`) %>% 
  mutate('Box Number' = row_number()) %>%
  select(c('Order Number', 'Order Size', 'Box Number', 'Box Size', 'Soaps in Box'))
  
View(boxes_per_order)
View(soaps_per_box)

