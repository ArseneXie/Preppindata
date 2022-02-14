import pandas as pd

grade_points = {'A':10, 'B':8, 'C':6, 'D':4, 'E':2, 'F':1}

score = pd.read_csv(r'C:/Data/PreppinData/PD 2022 Wk 5 Input.csv')
score = score.melt(id_vars='Student ID', var_name='Subject', value_name='Score')
score = score.sort_values(['Subject', 'Score', 'Student ID'], ascending=[True, False, True]).reset_index()
score['Dummy'] = score.index
score['Grade'] = score.groupby(['Subject'])['Dummy'].transform(lambda x: pd.qcut(x, len(grade_points), labels=list(grade_points.keys())))
score['Points'] = score['Grade'].apply(lambda x: grade_points[x]).astype(int)

score['Total points per Student'] = score['Points'].groupby(score['Student ID']).transform('sum')
score['Avg student total points per grade'] = round(score['Total points per Student'].groupby(score['Grade']).transform('mean'), 2)

score['Student Total Score'] = score['Score'].groupby(score['Student ID']).transform('sum')
score['Avg Total Score with one A'] = score[score['Grade']=='A'][['Student ID', 'Student Total Score']].drop_duplicates()['Student Total Score'].mean()

score = score[(score['Student Total Score']>=score['Avg Total Score with one A']) & (score['Grade']!='A')].copy()

final = score[['Student ID', 'Score', 'Subject', 'Points', 'Grade', 'Total points per Student', 'Avg student total points per grade']].copy()

quest = score.copy()
quest['Student Total Score'] = quest['Score'].groupby(quest['Student ID']).transform('sum')
quest = quest[quest['Student Total Score']>=quest['Avg Total Score with one A']][['Student ID']].nunique()[0]
