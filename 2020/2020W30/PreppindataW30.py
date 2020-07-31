#pip install google_spreadsheet
#pip install google-auth-oauthlib
import pandas as pd
import re
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SHEET_ID = '1ZJgR0PKIa4hvc3Pk5Y4cnvd9Cdk5klgXthc63vPQZ-4'

global values_input, service
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'F:\\Auth\\credentials.json', SCOPES) 
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()

def get_data(xrange):
    result_input = sheet.values().get(spreadsheetId=SHEET_ID,range=xrange).execute()
    values_input = result_input.get('values', [])
    return values_input    

sheet_metadata = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
properties = sheet_metadata.get('sheets')
df = []
for item in properties:
    sheet_name = item.get('properties').get('title')
    temp = get_data(sheet_name)
    temp_df = pd.DataFrame(temp[1:], columns=temp[0])
    temp_df['Forecast Type'] = sheet_name
    df.append(temp_df)    
    
def as_int(ival):
    try:
        oval = int(ival)
    except ValueError:
        oval = None    
    return oval    

final = pd.concat(df).reset_index(drop=True)
final['Data'] = final['Data'].str.replace('\n','|')
final['Date or Time'] = final['Data'].apply(lambda x: x.split(sep='|')[0])
final['Temperature'] = final.apply(lambda x: as_int(re.sub('\D','',x['Data'].split(sep='|')[1])) if x['Forecast Type']!='Next 5 Days' else None, axis=1)
final['Precipitation Chance'] = final.apply(lambda x: as_int(re.sub('\D','',x['Data'].split(sep='|')[2 if x['Forecast Type']!='Next 5 Days' else 3])), axis=1)
final['Max Temp'] = final.apply(lambda x: as_int(re.sub('\D','',x['Data'].split(sep='|')[1])) if x['Forecast Type']=='Next 5 Days' else None, axis=1)
final['Min Temp'] = final.apply(lambda x: as_int(re.sub('\D','',x['Data'].split(sep='|')[2])) if x['Forecast Type']=='Next 5 Days' else None, axis=1)
final = final.drop('Data', axis=1)