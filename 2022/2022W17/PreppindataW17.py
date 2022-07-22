import pandas as pd
import re

xlsx = pd.ExcelFile(r"C:\Data\PreppinData\2022W17 Input.xlsx")

stream = pd.read_excel(xlsx, 'Streaming')
stream['timestamp'] = stream['t'].apply(lambda x: pd.to_datetime(re.sub('[A-Z]',' ',x)))
stream['location'] = stream['location'].str.replace('Edin.*','Edinburgh',regex=True)
stream['content_type'] = stream.apply(lambda x: 'Primary' if re.search('(London|Cardiff|Edinburgh)', x['location']) else 
                                      'Secondary' if pd.isna(x['content_type']) else x['content_type'], axis=1)
stream = stream.groupby(['userID', 'timestamp', 'location', 'content_type'], as_index=False).agg({'duration':'sum'})

stream['dummy_location'] = stream.apply(lambda x: 'dummy' if x['content_type']=='Primary' else x['location'], axis=1)

stream['min timestamp'] = stream['timestamp'].groupby([stream['userID'], stream['content_type'], stream['dummy_location']]).transform('min')
stream['Month'] = stream['min timestamp'].apply(lambda x: x.strftime('%m %Y'))

final = pd.merge(stream, pd.read_excel(xlsx, 'Avg Pricing').rename(columns={'Content_Type':'content_type'}), on=['Month', 'content_type'], how='left')
final['Avg_Price'] = final.apply(lambda x: 14.98 if x['content_type']=='Preserved' else x['Avg_Price'], axis=1) 

final = final[['userID', 'timestamp', 'location', 'content_type', 'duration', 'Avg_Price']]
