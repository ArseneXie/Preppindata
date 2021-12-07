library(readxl)
library(dplyr)
library(purrr)

xlsx <- "C:/Data/PreppinData/Bookshop.xlsx"

final <- read_excel(xlsx, 'Book') %>%
  merge(., read_excel(xlsx, 'Author'), by='AuthID', all.x=TRUE) %>%
  merge(., read_excel(xlsx, 'Info') %>% 
          mutate('BookID'=paste0(`BookID1`,`BookID2`)) %>% select(-c('BookID1','BookID2')), by='BookID', all.x=TRUE) %>%
  merge(., read_excel(xlsx, 'Series'), by='SeriesID', all.x=TRUE) %>%
  merge(., read_excel(xlsx, 'Award') %>% 
          group_by(`Title`) %>% summarise('Number of Awards' = n()), by='Title', all.x=TRUE) %>% 
  merge(., read_excel(xlsx, 'Checkouts') %>% 
          group_by(`BookID`) %>% summarise('Number of Months Checked Out' = n_distinct(`CheckoutMonth`), 
                                           'Total Checkouts'=sum(`Number of Checkouts`)), by='BookID', all.x=TRUE) %>% 
  merge(., read_excel(xlsx, 'Ratings') %>% 
          group_by(`BookID`) %>% summarise('Average Rating' = mean(`Rating`), 
                                           'Number of Reviewers' = n_distinct(`ReviewerID`),
                                           'Number of Reviews'=n() ), by='BookID', all.x=TRUE) %>% 
  merge(., read_excel(xlsx, 'Edition'), by='BookID', all.y=TRUE) %>%
  merge(., read_excel(xlsx, 'Publisher'), by='PubID', all.x=TRUE) %>%
  merge(., xlsx %>% excel_sheets() %>% .[grepl('^Sales.*',.)] %>%
          map_df( ~ read_excel(path = xlsx, sheet = .x,)), by='ISBN', all.y=TRUE) %>%
  select(c('BookID', 'Sale Date', 'ISBN', 'Discount', 'ItemID', 'OrderID', 
           'First Name', 'Last Name', 'Birthday', 'Country of Residence', 'Hrs Writing per Day',
           'Title', 'AuthID', 'Format', 'PubID', 'Publication Date', 'Pages', 'Print Run Size (k)',
           'Price', 'Publishing House', 'City', 'State', 'Country', 'Year Established', 'Marketing Spend',
           'Number of Awards', 'Number of Months Checked Out', 'Total Checkouts',
           'Genre', 'SeriesID', 'Volume Number', 'Staff Comment', 'Series Name', 'Planned Volumes', 'Book Tour Events',
           'Average Rating', 'Number of Reviewers', 'Number of Reviews'))

View(final)
