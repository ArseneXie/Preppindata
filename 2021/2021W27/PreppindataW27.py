import pandas as pd
import random

xlsx = pd.ExcelFile("F:/Data/PD 2021 Wk 27 Input.xlsx")

team = pd.read_excel(xlsx,sheet_name='Teams')
seeding = pd.read_excel(xlsx,sheet_name='Seeding')

teams = team['Seed'].tolist()
temp = []

for rnd in range(1,5):
    pick = random.choices(teams, weights=tuple(list(seeding[rnd])), k=1)[0]
    df = team[team['Seed']==pick].copy()
    df['Actual Pick'] = rnd
    temp.append(df)
    
    teams.remove(pick)
    seeding = seeding[seeding['Seed']!=pick].copy()
    
picked = pd.concat(temp)

remain = team[team['Seed'].isin(teams)].copy()
remain['Actual Pick'] = remain['Seed'].rank(ascending=True).astype(int)+rnd
    
final = pd.concat([picked, remain])[['Actual Pick', 'Seed', 'Team']].rename(columns={'Seed':'Original'})
