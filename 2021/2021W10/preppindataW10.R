library(readxl)
library(dplyr)
library(stringr)

xlsx <- "F:/Data/Pokemon Input.xlsx"
  
pokemon <- read_excel(xlsx, sheet = "Pokemon") %>%
  filter(!str_detect(`Name`,'^Mega\\s')) %>%
  filter(as.numeric(str_trim(`#`))<=386) %>%
  select(-'Type') %>%
  distinct()

evolution <- read_excel(xlsx, sheet = "Evolution") %>%
  distinct() %>%
  filter(`Evolving to` %in% pokemon$Name) %>%
  rename('Name'='Evolving from') %>%
  merge(., dk,by.x='Name', by.y='Evolving to')

  merge(. %>% rename('Name'='Evolving from'),. %>% select(c('Evolving from', 'Evolving to')),  by.x='Name', by.y='Evolving to')
  
  merge(. %>% rename('Name'='Evolving from'),. %>% select(c('Evolving from', 'Evolving to')),  by.x='Name', by.y='Evolving to')
  

dk <- evolution  %>% select(c('Evolving from', 'Evolving to'))

get_rule <-function (df){
  out <- df %>%  
  return out
}
  
  final <- read_excel(, sheet = "OfficialMoney",
                      col_types = c("text", "numeric", "numeric", "text")) %>%  

    plot(df_g)
    
library(igraph)   
library(tidyr)  
library(purrr)
  
df <-   evolution %>%
  select(c('Evolving from', 'Evolving to'))

dk <- df %>%
  filter(!(`Evolving from` %in% df$`Evolving to`)) %>%
  mutate('Evolving to'=`Evolving from`,
         'Evolving from'="root2")

ds <- rbind(df,dk)

ds <- data.frame(name = c("land", "water", "air", "car", "bicycle", "boat", "balloon", "airplane", "helicopter", "Ford", "BMW", "Airbus"), 
                 parent = c("root", "root", "root", "land", "land", "water", "air", "air", "air", "car", "car", "airplane"))

library(data.tree)  
tkt <- ToDataFrameTree(ds)

print(tkt, limit = 15)

tree <- FromDataFrameNetwork(ds)
#Getting the required format then becomes trivial as we can use the hierarchy infrastructure from data.tree:
  
tkt<- ToDataFrameTree(tree, 
                level1 = function(x) x$path[2],
                level2 = function(x) x$path[3],
                level3 = function(x) x$path[4],
                level_number = function(x) x$level - 1)[-1,-1]

print(tkt, limit = 15)

plot(tkt)

tkt$Climb(position = c(2, 3, 4))$path

V(df_g)
subcomponent(df_g, .x, mode="out")

?subcomponent

df_g = graph_from_data_frame(df, directed=TRUE)


e = get.edgelist(df_g)

# Root vertices are in first column but not in second column
root = setdiff(e[,1],e[,2])

# Terminal vertices are in second column but not in first column
terminal = setdiff(e[,2], e[,1])

# Vertices to remove are not in root or terminal vertices
remove = setdiff(unique(c(e)), c(root, terminal))

# Remove names of intermediate vertices
V(df_g)$name[V(df_g)$name %in% remove] = ""

SOURCES <- which(sapply(names(V(df_g)), function(x) length(neighbors(df_g, x, mode="in"))) == 0)
SINKS   <- which(sapply(names(V(df_g)), function(x) length(neighbors(df_g, x, mode="out"))) == 0)
INTERMED <- setdiff(names(V(df_g)), c(SINKS, SOURCES))

## Fix up the node names and plot
V(df_g)$name = names(V(df_g))
V(df_g)$name[INTERMED] = ""

as_data_frame()


wanted_df2 <- map(V(df_g), ~ names(subcomponent(df_g, .x, mode="out"))) %>% 
  map_df(~data.frame(Name=.x), .id="Evolution Group") %>%
  mutate('Test' = sapply(V(df_g), ~ length(neighbors(df_g, .x, mode="in"))) == 0)
           

test <- as_data_frame(df_g, what="vertices")

?subcomponent
?graph_from_data_frame

wanted_df2 = map(V(df_g), ~ names(subcomponent(df_g, .x, mode="out"))) %>% 
  map_df(~data.frame(Name=.x), .id="Evolution Group") %>% 
  # Get rid of rows where `pid` and `cid` are equal
  filter(Evolving_to != Evolving_from) %>% 
  # Convert columns (from character) to numeric. Not necessary, but this makes the columns the same mode as the columns in `wanted_df`.
  mutate(pid=as.numeric(pid),
         cid=as.numeric(cid))
    
final <- read_excel("F:/Data/Customer Information.xlsx") %>%
  cSplit(., 'IDs', ' ') %>%
  pivot_longer(everything(), names_to = c(".value",NA), names_pattern = '(ID)(.*)', values_drop_na=TRUE) %>%
  mutate('Phone' = str_extract(`ID`,'(\\d{6})(?=,)'),
         'Area Code Key' = str_extract(`ID`,'(?<=,)(\\d{2}[A-Z])'),
         'Product ID' = str_extract(`ID`,'([A-Z]+)$'),
         'Quantity' = as.integer(str_extract(`ID`,'(\\d+)(?=-)'))) %>%
  filter(`Quantity`>0) %>%
  merge(.,read_excel("F:/Data/Area Code Lookup.xlsx") %>%
          filter(!(`Area` %in% c('Clevedon', 'Fakenham', 'Stornoway'))) %>%
          mutate('Area Code Key' = paste0(str_sub(`Code`,-2),str_sub(`Area`,1,1))) %>%
          group_by(`Area Code Key`) %>%
          filter(n()==1), by='Area Code Key') %>%
  merge(.,read_excel("F:/Data/Product Lookup.xlsx") %>%
          mutate('Price' = as.numeric(str_sub(`Price`,2))), by='Product ID') %>%
  group_by(`Area`,`Product Name`) %>%
  summarise('Revenue' = round_half_up(sum(`Price`*`Quantity`)),
            .groups='drop') %>%
  group_by(`Area`) %>%
  mutate('Rank' = dense_rank(desc(`Revenue`)),
         '% of Total ¡V Product' = round_half_up(`Revenue`/sum(`Revenue`)*100,2)) %>%
  select(c('Rank', 'Area', 'Product Name', 'Revenue', '% of Total ¡V Product'))
 
View(final)
