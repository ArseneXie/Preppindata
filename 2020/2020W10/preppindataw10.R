library(magrittr)
library(ompr)
library(ompr.roi)
library(ROI.plugin.glpk)
library(dplyr)
library(knitr)
library(kableExtra)

n <- 4

model4 <- MILPModel() %>%
  # 6 grids:
  add_variable(xTL[i, j], i = 1:n, j = 1:n, type = "binary") %>%
  add_variable(xTX[i, j], i = 1:n, j = 1:n, type = "binary") %>%
  add_variable(xXL[i, j], i = 1:n, j = 1:n, type = "binary") %>%
  add_variable(xTP[i, j], i = 1:n, j = 1:n, type = "binary") %>%
  add_variable(xPL[i, j], i = 1:n, j = 1:n, type = "binary") %>%
  add_variable(xPX[i, j], i = 1:n, j = 1:n, type = "binary") %>%
  
  # No objective:
  set_objective(0) %>%
  
  # Only one cell can be assigned in a row:
  add_constraint(sum_expr(xTL[i, j], j = 1:n) == 1, i = 1:n) %>%
  add_constraint(sum_expr(xTX[i, j], j = 1:n) == 1, i = 1:n) %>%
  add_constraint(sum_expr(xXL[i, j], j = 1:n) == 1, i = 1:n) %>%
  add_constraint(sum_expr(xTP[i, j], j = 1:n) == 1, i = 1:n) %>%
  add_constraint(sum_expr(xPL[i, j], j = 1:n) == 1, i = 1:n) %>%
  add_constraint(sum_expr(xPX[i, j], j = 1:n) == 1, i = 1:n) %>%
  
  # Only one cell can be assigned in a column:
  add_constraint(sum_expr(xTL[i, j], i = 1:n) == 1, j = 1:n) %>%
  add_constraint(sum_expr(xTX[i, j], i = 1:n) == 1, j = 1:n) %>%
  add_constraint(sum_expr(xXL[i, j], i = 1:n) == 1, j = 1:n) %>%
  add_constraint(sum_expr(xTP[i, j], i = 1:n) == 1, j = 1:n) %>%
  add_constraint(sum_expr(xPL[i, j], i = 1:n) == 1, j = 1:n) %>%
  add_constraint(sum_expr(xPX[i, j], i = 1:n) == 1, j = 1:n) %>%
  
  #Additional
  add_constraint(xTL[i, j] + xTX[i, k] <= xXL[k, j] + 1, i = 1:n, j = 1:n, k = 1:n) %>%
  add_constraint(xTL[i, j] + xTP[i, k] <= xPL[k, j] + 1, i = 1:n, j = 1:n, k = 1:n) %>%
  add_constraint(xTX[i, j] + xTP[i, k] <= xPX[k, j] + 1, i = 1:n, j = 1:n, k = 1:n) %>%
  add_constraint(xPL[i, j] + xPX[i, k] <= xXL[k, j] + 1, i = 1:n, j = 1:n, k = 1:n)

model4_fixed <- model4 %>%
  # Clue1 Only the customer with the highest priority has a title and last name that begin with the same letter.
  add_constraint(xTL[1, 3] + xTL[2, 2] + xTL[3, 4] + xTL[4, 1] == 1) %>% 
  add_constraint(xTL[1, 3] == xTP[1, 1]) %>% 
  add_constraint(xTP[1, 1] == xPL[1, 3]) %>%
  add_constraint(xTL[2, 2] == xTP[2, 1]) %>% 
  add_constraint(xTP[2, 1] == xPL[1, 2]) %>%
  add_constraint(xTL[3, 4] == xTP[3, 1]) %>% 
  add_constraint(xTP[3, 1] == xPL[1, 4]) %>%
  add_constraint(xTL[4, 1] == xTP[4, 1]) %>% 
  add_constraint(xTP[4, 1] == xPL[1, 1]) %>%
  
  # Clue2a Bevens(L1) priority is directly after Dimmadome(L3)
  add_constraint(xPL[1, 1] == 0) %>% # Bevens(L1) cannot be 1st
  add_constraint(xPL[4, 3] == 0) %>% # Dimmadome(L3) cannot be 4th
  add_constraint(sum_expr(i * xPL[i, 1], i = 1:4) == sum_expr(i * xPL[i, 3], i = 1:4) + 1) %>% 
  # Clue2b Neither of these people(L1,L3) ordered the Chamomile Bar(X3) or the Hibiscus Soap-on-a-Rope(X4).
  add_constraint(xXL[3, 1] == 0) %>% 
  add_constraint(xXL[3, 3] == 0) %>% 
  add_constraint(xXL[4, 1] == 0) %>% 
  add_constraint(xXL[4, 3] == 0) %>% 
  
  # Clue3 The Sergeant(T2) and the person who ordered Lemon Gel(X2) are either 1st priority(P1) or 3rd priority(P3)
  add_constraint(xTP[2, 1] + xTP[2, 3] == 1) %>% 
  add_constraint(xPX[1, 2] + xPX[3, 2] == 1) %>% 
  
  # Clue4 The Reverend(T3) didn't order the Rose Bar(X1) and isn't 2nd priority(P2).
  add_constraint(xTX[3, 1] == 0) %>% 
  add_constraint(xTP[3, 2] == 0) %>% 
  
  # Clue5 The Sergeant(T2) either ordered Hibiscus Soap-on-a-Rope(X4) or is 4th priority(P4)
  add_constraint(xTX[2, 4] + xTP[2, 4] >= 1) %>% 
  
  # Clue6 The priority of the person who ordered the Rose Bar(X1) is directly after the person who ordered the Lemon Gel(X2).
  add_constraint(xPX[1, 1] == 0) %>% # Rose Bar(X1) cannot be 1st(P1)
  add_constraint(xPX[4, 2] == 0) %>% # Lemon Gel(X2) cannot be 4th(P4)
  add_constraint(sum_expr(i * xPX[i, 1], i = 1:4) == sum_expr(i * xPX[i, 2], i = 1:4) + 1) %>%
  
  # Clue7 Dimmadome(L3) is not a Doctor(T1) and the Baroness(T4) didn't order the Hibiscus Soap-on-a-Rope(X4).
  add_constraint(xTL[1, 3] == 0) %>%
  add_constraint(xTX[4, 4] == 0) 
  
  

result <- solve_model(model4_fixed, with_ROI(solver = "glpk", verbose = TRUE))

Is <- c("Doctor", "Sergeant", "Reverend", "Baroness") # Title
Js <- c("Bevens", "Shadwell", "Dimmadome", "Rotzenheimer") # LastName
Ks <- c("Rose Bar", "Lemon Gel", "Chamomile Bar", "Hibiscus Soap-on-a-Rope") # Product
Ls <- as.character(1:4) # Priority

# Extract solved grids
solution <- list(
  xTL = get_solution(result, xTL[i, j]) %>%
    dplyr::filter(value == 1) %>%
    dplyr::select(-c(variable, value)) %>%
    dplyr::mutate(i = Is[i], j = Js[j]),
  xTX = get_solution(result, xTX[i, k]) %>%
    dplyr::filter(value == 1) %>%
    dplyr::select(-c(variable, value)) %>%
    dplyr::mutate(i = Is[i], k = Ks[k]),
  xTP = get_solution(result, xTP[i, l]) %>%
    dplyr::filter(value == 1) %>%
    dplyr::select(-c(variable, value)) %>%
    dplyr::mutate(i = Is[i], l = Ls[l]),
  xPL = get_solution(result, xPL[l, j]) %>%
    dplyr::filter(value == 1) %>%
    dplyr::select(-c(variable, value)) %>%
    dplyr::mutate(l = Ls[l], j = Js[j]),
  xPX = get_solution(result, xPX[l, k]) %>%
    dplyr::filter(value == 1) %>%
    dplyr::select(-c(variable, value)) %>%
    dplyr::mutate(l = Ls[l], k = Ks[k]),
  xXL = get_solution(result, xXL[k, j]) %>%
    dplyr::filter(value == 1) %>%
    dplyr::select(-c(variable, value)) %>%
    dplyr::mutate(k = Ks[k], j = Js[j])
)

# Obtained solution
solution %>%
  purrr::reduce(dplyr::left_join) %>%
  dplyr::arrange(l) %>%
  kable(col.names = c("Title", "LastName", "Product", "Priority"), align = "l") %>%
  kable_styling(bootstrap_options = c("striped"))