import pandas as pd
import re
import numpy as np

xlsx = pd.ExcelFile(r"F:\Data\Pictures Input.xlsx")

def analyze_size(size_str):
    side_a = float(re.search('^(\d+)', size_str).group(1))
    side_b = float(re.search('\D(\d+)\D', size_str).group(1) if re.search('\D(\d+)\D', size_str) else side_a)
    side_all = [side_a, side_b] if re.search('(cm)', size_str) else [side_a*2.54, side_b*2.54]
    side_all.sort()
    
    return side_all

picture = pd.read_excel(xlsx,'Pictures')
picture['Size Side'] = picture['Size'].apply(lambda x: analyze_size(x))
picture['Min Side'] = picture['Size Side'].apply(lambda x: x[0])
picture['Max Side'] = picture['Size Side'].apply(lambda x: x[1])

frame = pd.read_excel(xlsx,'Frames')
frame.columns = ['Frame']
frame['Frame Size Side'] = frame['Frame'].apply(lambda x: analyze_size(x))

final = pd.merge(picture, frame, how='cross')
final['Fit'] = final.apply(lambda x: x['Frame Size Side'][0]>=x['Size Side'][0] and x['Frame Size Side'][1]>=x['Size Side'][1], axis=1)
final = final[final['Fit']].copy()
final['Excess Area'] = final.apply(lambda x: np.prod(x['Frame Size Side'])-np.prod(x['Size Side']), axis=1)
final['Min Excess Area'] = final['Excess Area'].groupby(final['Picture']).transform('min')

final = final[final['Excess Area']==final['Min Excess Area']][['Picture', 'Frame', 'Max Side', 'Min Side']]
