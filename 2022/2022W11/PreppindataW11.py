import pandas as pd
import numpy as np

attend = pd.read_csv(r"C:\Data\PreppinData\PD Fill the Blanks challenge.csv")

attend = attend.sort_values(['Weekday', 'Lesson Time', 'Lesson Name'])
attend['Lesson Name'] = attend.groupby(['Weekday', 'Lesson Time'])['Lesson Name'].ffill()

attend = attend.sort_values(['Weekday', 'Lesson Time', 'Subject'])
attend['Subject'] = attend.groupby(['Weekday', 'Lesson Time'])['Subject'].ffill()

attend['Avg. Attendance per Subject & Lesson'] = attend.groupby(['Weekday', 'Lesson Name', 'Subject'])['Attendance'].transform(np.mean)
