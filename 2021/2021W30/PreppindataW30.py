import pandas as pd

lift = pd.read_csv("F:\\Data\\2021W30.csv")
lift = lift.sort_values(['Hour', 'Minute'], ascending=[True, True]).reset_index(drop=True)
lift = lift.replace({'From':{'G':0,'B':-1}, 'To':{'G':0,'B':-1}})
lift['From'] = lift['From'].astype('int')
lift['To'] = lift['To'].astype('int')
lift['Floors Btw Trips'] = abs(lift['From'] - lift['To'].shift(1))
lift['Default position'] = lift.groupby('From').count().Hour.idxmax()
lift['From Default Position'] = abs(lift['From'] - lift['Default position'])

final = lift.groupby('Default position', as_index=False).agg({'From Default Position':'mean', 'Floors Btw Trips':'mean'})
final['Difference'] = final['From Default Position'] - final['Floors Btw Trips'] 
final = final.rename(columns={'From Default Position':'Avg travel from default position', 'Floors Btw Trips':'Avg travel between trips currently'})
