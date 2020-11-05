import pandas as pd
import re
import fiscalyear
from datetime import datetime

costume_pt = {'Cat':'^[CKG].*at.*', 'Clown':'^[CK]l.*n$', 'Devil':'^D.*(ev|ia).*', 'Dinosaur':'^Dino.*', 'Ghost':'^G.*t$',
              'Pirate':'^Pira.*', 'Vampire':'^Vamp.*', 'Werewolf':'^We.*wolf$', 'Zombie':'^Z.*mbi.*'}
fiscalyear.START_MONTH = 11
xlsx = pd.ExcelFile("F:/Data/Halloween Costumes.xlsx")
df = pd.read_excel(xlsx,sheet_names=1)
df['Date'] = df['Date'].apply(lambda x: datetime.strptime(x,'%d/%m/%Y'))
df['FiscalYear'] = df['Date'].apply(lambda x: fiscalyear.FiscalDate(x.year, x.month, x.day).fiscal_year)
df = df[df['FiscalYear']>=2019].copy()
df['FiscalYear'] = df['FiscalYear'].apply(lambda x: f'{x} FY Sales')
for correct, pattern in costume_pt.items():
    df['Costume'] = df['Costume'].replace(to_replace = pattern, value = correct, regex = True)
df = df.replace({'Country': {'Indonsia': 'Indonesia', 'Slovnia': 'Slovenia', 'Philippins':'Philippines', 'Luxmbourg':'Luxembourg'}})    
final = df.melt(id_vars = [c for c in df.columns if not re.search('^Sales',c)],value_name = 'Draft Sales', var_name='Price').dropna()
final['Currency'] = final['Draft Sales'].apply(lambda x: re.sub('\s+\d+\.\d+','',x))
final['Sales'] = final['Draft Sales'].apply(lambda x: int(float(re.search('(\d+\.\d+$)',x).group(1))))
final['Price'] = final['Price'].apply(lambda x: re.search('(?<=at\s)(\w+)(?=\s)',x).group(1))
final = final.drop(['Date','Draft Sales'],axis=1).pivot_table(index = ['Costume', 'Country', 'Currency', 'Price'],
                                                         columns='FiscalYear',
                                                         values='Sales',
                                                         aggfunc={'Sales':'sum'})
final.reset_index(drop=False, inplace=True)
