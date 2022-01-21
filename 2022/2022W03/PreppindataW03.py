import pandas as pd

student = pd.read_csv(r'C:/Data/PreppinData/PD 2022 Wk 1 Input - Input.csv')
gender = {v[0]:v[1] for v in student[['id', 'gender']].T.to_dict('list').values()}

final = pd.read_csv(r'C:/Data/PreppinData/PD 2022 WK 3 Grades.csv')
sub_list = [c for c in final.columns if c != 'Student ID']
final["Student's Avg Score"] = round(final[sub_list].mean(axis=1),1)
final['Passed Subjects'] = final[sub_list].apply(lambda x: sum(x>=75), axis=1)
final['Gender'] = final['Student ID'].apply(lambda x: gender[x])
final = final[['Passed Subjects', "Student's Avg Score", 'Student ID', 'Gender']]
