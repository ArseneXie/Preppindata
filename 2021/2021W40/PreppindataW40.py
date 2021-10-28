import pandas as pd
import re

animal = pd.read_csv("C:\\Data\\PreppinData\\Austin_Animal_Center_Outcomes.csv")[['Animal Type', 'Outcome Type']]
animal = animal[animal['Animal Type'].isin(['Cat', 'Dog'])].copy()
animal['Outcome Type'] = animal['Outcome Type'].apply(lambda x: 'Adopted, Returned to Owner or Transferred'
                                                      if re.match('(Adoption|Return to Owner|Transfer)',str(x)) else 'Other')
animal['RowCount'] = 1

final = animal.groupby(['Animal Type', 'Outcome Type']).agg({'RowCount':'sum'})
final['Ratio'] = final['RowCount'].groupby(level=0).apply(lambda x: round(x*100/float(x.sum()),1))
final = final.reset_index(drop=False)
final = final.pivot_table(index='Animal Type', columns='Outcome Type', values='Ratio', aggfunc=max).reset_index()
