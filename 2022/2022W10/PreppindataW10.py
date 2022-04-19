import pandas as pd
import html
import re

xlsx = pd.ExcelFile(r"C:\Data\PreppinData\PD Bechdel Test.xlsx")

ranking = {"There are two or more women in this movie and they talk to each other about something other than a man":1,
           "There are two or more women in this movie and they talk to each other about something other than a man, although dubious":2,
           "There are two or more women in this movie, but they only talk to each other about a man":3,
           "There are two or more women in this movie, but they don't talk to each other":4,
           "Fewer than two women in this movie":5 }

movie = pd.read_excel(xlsx,'Webscraping')
movie['Movie'] = movie['DownloadData'].apply(lambda x: html.unescape(re.search('(?<=>)(([^><])+)(?=<\/a>)', x).group(1)))
movie['Categorisation'] = movie['DownloadData'].apply(lambda x: re.search('(?<=title="\[)(.*)(?=\])', x).group(1))
movie['Ranking'] = movie['Categorisation'].apply(lambda x: ranking.get(x))
movie['Worst Ranking'] = movie['Ranking'].groupby([movie['Movie'], movie['Year']]).transform('max')
movie = movie[movie['Ranking'] == movie['Worst Ranking']].drop('DownloadData', axis=1).drop_duplicates()
movie['Pass/Fail'] = movie['Ranking'].apply(lambda x: 'Pass' if x<=2 else 'Fail')
movie = movie[['Movie', 'Year', 'Pass/Fail', 'Ranking', 'Categorisation']]
