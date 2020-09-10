import pandas as pd
from math import ceil

xlsx = pd.ExcelFile("F:/Data/School Timetables-4.xlsx")
teacher = pd.read_excel(xlsx,'Teachers')   
student = pd.read_excel(xlsx,'Students')   
room = pd.read_excel(xlsx,'Rooms')   
hours = pd.read_excel(xlsx,'Hours')   

needed = pd.concat([student.drop('Subject',axis=1), 
                    pd.DataFrame([x for x in student['Subject'].str.split('/').values.tolist()])], axis=1, sort=False)
needed = needed.melt(id_vars=['Name','Age'], value_name='Subject', var_name='To_drop').dropna().drop('To_drop',axis=1)
needed['dummy'] = 'd'

temp = hours['Age Group'].str.split('-', n = 1, expand = True) 
hours['fromAge'] = temp[0] .astype('int64') 
hours['toAge'] = temp[1].astype('int64') 
hours['dummy'] = 'd'

needed = needed.merge(hours, on='dummy')
needed = needed[(needed['Age']>=needed['fromAge']) & (needed['Age']<=needed['toAge'])].drop(['dummy','fromAge','toAge'],axis=1)

temp = teacher['Ages Taught'].str.split('-', n = 1, expand = True) 
teacher['fromAge'] = temp[0] .astype('int64') 
teacher['toAge'] = temp[1].astype('int64') 

supply = pd.concat([teacher.drop(['Working Days','Ages Taught'],axis=1), 
                    pd.DataFrame([x for x in teacher['Working Days'].str.split(',').values.tolist()])], axis=1, sort=False)
supply = supply.melt(id_vars=['Name','Subject','fromAge','toAge'], value_name='Working Days', var_name='To_drop').dropna().drop('To_drop',axis=1)
supply['Allocated Hours'] = 6/supply['Subject'].groupby([supply['Name'],supply['Working Days']]).transform('count')
supply['Potential Teachers Hours'] = supply['Allocated Hours'].groupby(supply['Subject']).transform('sum')
supply = supply.drop(['Working Days','Allocated Hours'],axis=1).drop_duplicates()

demand = needed.groupby(['Subject','Age'], as_index=False).agg({'Hours teaching per week':'first', 'Name':'count'})
demand = demand.rename(columns={'Name':'Students Count'})

room = room.groupby('Subjects', as_index=False).agg({'Capacity':'sum'})
room = room.rename(columns={'Subjects':'Subject'})

final = pd.merge(supply, demand, on='Subject')
final = final[(final['Age']>=final['fromAge']) & (final['Age']<=final['toAge'])].drop(['fromAge','toAge'],axis=1)
final = pd.merge(final, room, on='Subject')
final['Classes required'] = final.apply(lambda x: ceil(x['Students Count']/x['Capacity']), axis=1)
final['Total Teaching Hours needed'] = final.apply(lambda x: x['Classes required']*x['Hours teaching per week'], axis=1)
final = final.groupby(['Subject'], as_index=False).agg({'Potential Teachers Hours':'first',
                                                        'Total Teaching Hours needed':'sum',
                                                        'Classes required':'sum'})
final['% utilised'] = round(final['Total Teaching Hours needed']/final['Potential Teachers Hours']*100)
