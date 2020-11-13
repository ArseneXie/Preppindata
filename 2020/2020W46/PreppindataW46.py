import pandas as pd
import re
from datetime import datetime as dt

xlsx = pd.ExcelFile("F:/Data/Incident List.xlsx")

incident = pd.read_excel(xlsx,'Incident List')
incident['Aircraft'] = incident['Incident'].apply(lambda x: re.search('(.*?)(?=\s(at|near)\s)',x).group(1)) 
incident['Date'] = incident['Incident'].apply(lambda x: dt.strptime(
    re.sub('.*([A-Z][a-z]{2})\s(\d+)[a-z]{2}\s(\d{4}).*','\\2-\\1-\\3',x),'%d-%b-%Y').date()) 
incident['Location'] = incident['Incident'].apply(lambda x: re.search('(?<=at\s)(.*?)(?=\son\s)',x).group(1) 
                                                  if re.search('(?<=at\s)(.*?)(?=\son\s)',x) else re.search('(?<=near\s)(.*?)(?=\son\s)',x).group(1))
incident['Incident Description'] = incident['Incident'].apply(lambda x: re.search('(?<=\d{4},\s)(.*$)',x).group(1)) 
finalA = incident[['Date', 'Location', 'Aircraft', 'Incident Description']]

finalB = pd.read_excel(xlsx,'Category') 
finalB['Number of Incidents'] = finalB['Category'].apply(lambda x: len([idt for idt in incident['Incident Description'].tolist() 
                                                                        if re.search(f"({x[0:5].lower()})",idt)]))
