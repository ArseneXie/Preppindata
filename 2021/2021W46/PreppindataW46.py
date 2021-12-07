import pandas as pd
import re

xlsx = pd.ExcelFile(r"C:\Data\PreppinData\Bookshop.xlsx")
book = pd.read_excel(xlsx,'Book')
author = pd.read_excel(xlsx,'Author')
info = pd.read_excel(xlsx,'Info')
award = pd.read_excel(xlsx,'Award')
checkouts = pd.read_excel(xlsx,'Checkouts')
edition = pd.read_excel(xlsx,'Edition')
publisher = pd.read_excel(xlsx,'Publisher')
ratings = pd.read_excel(xlsx,'Ratings')
series = pd.read_excel(xlsx,'Series')
temp = []
for sheet in [sh for sh in xlsx.sheet_names if re.match('^Sales.*',sh)]:
    df = pd.read_excel(xlsx,sheet)
    temp.append(df)
sales = pd.concat(temp)   

book = book.merge(author, on='AuthID')
info['BookID'] = info['BookID1']+info['BookID2'].astype(str)
info = info.merge(series, how='left', on='SeriesID').drop(['BookID1', 'BookID2'], axis=1)
edition = edition.merge(publisher, on='PubID')
award = award.groupby(["Title"], as_index=False).agg({'Award Name':'count'})
award = award.rename(columns={'Award Name':'Number of Awards'})
checkouts = checkouts.groupby(["BookID"], as_index=False).agg({'CheckoutMonth':'nunique', 'Number of Checkouts':'sum'})
checkouts = checkouts.rename(columns={'CheckoutMonth':'Number of Months Checked Out', 'Number of Checkouts':'Total Checkouts'})
ratings = ratings.groupby(["BookID"], as_index=False).agg({'Rating':'mean', 'ReviewerID':'nunique', 'ReviewID':'count'})
ratings = ratings.rename(columns={'Rating':'Average Rating', 'ReviewerID':'Number of Reviewers', 'ReviewID':'Number of Reviews'})

final = book.merge(info, how='left', on='BookID')
final = final.merge(award, how='left', on='Title')
final = final.merge(checkouts, how='left', on='BookID')
final = final.merge(ratings, how='left', on='BookID')
final = edition.merge(final, how='left', on='BookID')
final = sales.merge(final, how='left', on='ISBN')

final = final[['BookID', 'Sale Date', 'ISBN', 'Discount', 'ItemID', 'OrderID', 
               'First Name', 'Last Name', 'Birthday', 'Country of Residence', 'Hrs Writing per Day',
               'Title', 'AuthID', 'Format', 'PubID', 'Publication Date', 'Pages', 'Print Run Size (k)',
               'Price', 'Publishing House', 'City', 'State', 'Country', 'Year Established', 'Marketing Spend',
               'Number of Awards', 'Number of Months Checked Out', 'Total Checkouts',
               'Genre', 'SeriesID', 'Volume Number', 'Staff Comment', 'Series Name', 'Planned Volumes', 'Book Tour Events',
               'Average Rating', 'Number of Reviewers', 'Number of Reviews']]
