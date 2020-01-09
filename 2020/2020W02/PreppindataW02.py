import pandas as pd
import re

def format_time(tstr):
    return str(int(re.search(r'(\d+)(?=\d{2})',tstr).group(1))+
               (12 if  re.search(r'(p|P)',tstr) else 0)).zfill(2) + ':' + re.search(r'(\d{2})(?=\D|$)',tstr).group(1)

final = pd.read_csv(r'E:/PD 2020 Wk 2 Input - Time Inputs.csv' )
final['Time'] = final['Time'].apply(lambda x: format_time(re.sub('\s|\W','',x)))
final['Date Time'] = pd.to_datetime(final['Date'] + ' ' + final['Time'], format='%m/%d/%y %H:%M')
final['Date'] = final['Date Time'].dt.date
