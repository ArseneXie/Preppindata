import pandas as pd

def check_answer(myans, correct):
    ok = [r for r,a in zip(myans, correct) if r==a]
    return len(list(filter((',').__ne__,ok)))

xlsx = pd.ExcelFile("F:/Data/Quiz Results.xlsx")

ans = pd.read_excel(xlsx,'Participant Answers')
correct = pd.read_excel(xlsx,'Correct Answers')

final = ans.melt(id_vars='Name',var_name='Round', value_name='Result')
final = final.merge(correct, on='Round')
final['Score'] = final.apply(lambda x: check_answer(x['Result'],x['Answers']),axis=1)

final = final.pivot_table(index='Name', values='Score', columns='Round').reset_index()
final['Total Score'] = final['Round1'] + final['Round2'] + final['Round3'] + final['Round4'] + final['Round5'] 
final['Position'] = final['Total Score'].rank(ascending=False,method='dense').astype(int)
final = final[['Position','Name', 'Round1', 'Round2', 'Round3', 'Round4', 'Round5', 'Total Score']]
