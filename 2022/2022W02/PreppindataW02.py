import pandas as pd

final = pd.read_csv(r'C:/Data/PreppinData/PD 2022 Wk 1 Input - Input.csv',
                    parse_dates=['Date of Birth'], date_parser=lambda x: pd.to_datetime(x, format='%m/%d/%Y'))
final = final[['pupil first name', 'pupil last name', 'Date of Birth']]
final["Pupil's Name"] = final['pupil first name']+' '+final['pupil last name']
final["This Year's Birthday"] = final['Date of Birth'].apply(lambda x: x.replace(year = 2022))
final['Month'] = final["This Year's Birthday"].dt.strftime('%B')
final['Cake Needed On'] = final["This Year's Birthday"].dt.strftime('%A')
final = final.replace({'Cake Needed On':{'Saturday':'Friday','Sunday':'Friday'}})
final['BDs per Weekday and Month'] = final["Pupil's Name"].groupby([final['Month'], final['Cake Needed On']]).transform('count')
final['Date of Birth'] = final['Date of Birth'].dt.date
final["This Year's Birthday"] = final["This Year's Birthday"].dt.date
final = final[["Pupil's Name", "Date of Birth", "This Year's Birthday", "Month", "Cake Needed On", "BDs per Weekday and Month"]]
