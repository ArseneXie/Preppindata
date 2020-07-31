import pandas as pd
import re

xlsx = pd.ExcelFile("F:/Data/PD Olympics.xlsx")

def roman_to_int(rom):
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    out = 0
    for c,n in zip(rom,rom[1:]+rom[-1:]) :
        out = out + (1 if roman_map[c]>=roman_map[n] else -1)*roman_map[c]
    return out    
    
df = pd.read_excel(xlsx,sheet_name=0).dropna(subset=['Dates'])   
df = df[['Games', 'Host', 'Dates', 'Nations', 'Sports', 'Events']].copy()
df['Start Date'] = df.apply(lambda x: str(1896+4*(roman_to_int(x['Games'])-1))+'-'+
                            re.search('([A-Za-z]+)', x['Dates']).group(1)+'-'+
                            re.search('(\d+)\D+(\d+)', x['Dates']).group(1), axis=1)
df['End Date'] = df.apply(lambda x: str(1896+4*(roman_to_int(x['Games'])-1))+'-'+
                            re.search('([A-Za-z]+)$', x['Dates']).group(1)+'-'+
                            re.search('(\d+)\D+(\d+)', x['Dates']).group(2), axis=1)
df['Start Date'] = df['Start Date'].apply(lambda x: pd.to_datetime(x, format='%Y-%B-%d').date())
df['End Date'] = df['End Date'].apply(lambda x: pd.to_datetime(x, format='%Y-%B-%d').date())

final = df[['Start Date', 'End Date','Games', 'Host', 'Nations', 'Sports', 'Events']].copy()
