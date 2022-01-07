import pandas as pd
import fiscalyear

fiscalyear.START_MONTH = 9
final = pd.read_csv(r'C:/Data/PreppinData/PD 2022 Wk 1 Input - Input.csv',
                    parse_dates=['Date of Birth'], date_parser=lambda x: pd.to_datetime(x, format='%m/%d/%Y'))
final['Pupil\'s Name'] = final['pupil last name']+', '+final['pupil first name']
final['parent first name'] = final.apply(lambda x: x['Parental Contact Name_1'] if x['Parental Contact']==1 else x['Parental Contact Name_2'], axis=1)
final['Parental Contact Full Name'] = final['pupil last name']+', '+final['parent first name']
final['Parental Contact Email Address'] = final['parent first name']+'.'+final['pupil last name']+'@'+final['Preferred Contact Employer']+'.com'
final['Academic Year'] = final['Date of Birth'].apply(lambda x: 2016 - min(fiscalyear.FiscalDate(x.year, x.month, x.day).fiscal_year,2015))
final = final[['Academic Year', 'Pupil\'s Name', 'Parental Contact Full Name', 'Parental Contact Email Address']]
