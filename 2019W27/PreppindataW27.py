import pandas as pd
import datetime

sales = pd.read_excel(pd.ExcelFile(r"E:\PD - Week 27.xlsx"),"Sheet1") 
sales['Date'] = sales['Date'].apply(lambda x: x.date())
sales['Pre/Post Valentines Day'] = sales['Date'].apply(lambda x: 'Pre' if x<=datetime.date(2019, 2, 14) else 'Post')
sales['Running Total Sales']=sales.sort_values('Date').groupby(['Pre/Post Valentines Day','Store'])['Value'].cumsum()
sales.rename(columns={'Value': 'Daily Store Sales'}, inplace=True)






import matplotlib.pyplot as plt
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)  


ax1.get_shared_y_axes().join(ax1, ax2)
ax12 = ax1.twinx() 
ax22 = ax2.twinx() 
ax12.get_shared_y_axes().join(ax12, ax22)
temp = sales[(sales['Pre/Post Valentines Day']=='Pre') & (sales['Store']=='Leeds')]
ax1.plot(temp['Date'], temp['Running Total Sales'], color='red')
ax12.plot(temp['Date'], temp['Daily Store Sales'], color='blue')

temp = sales[(sales['Pre/Post Valentines Day']=='Post') & (sales['Store']=='Leeds')]
ax2.plot(temp['Date'], temp['Running Total Sales'], color='red')
ax22.plot(temp['Date'], temp['Daily Store Sales'], color='blue')


ax3.get_shared_y_axes().join(ax3, ax4)
ax32 = ax3.twinx() 
ax42 = ax4.twinx() 
ax32.get_shared_y_axes().join(ax32, ax42)

temp = sales[(sales['Pre/Post Valentines Day']=='Pre') & (sales['Store']=='York')]
ax3.plot(temp['Date'], temp['Running Total Sales'], color='red')
ax32.plot(temp['Date'], temp['Daily Store Sales'], color='blue')

temp = sales[(sales['Pre/Post Valentines Day']=='Post') & (sales['Store']=='York')]
ax4.plot(temp['Date'], temp['Running Total Sales'], color='red')
ax42.plot(temp['Date'], temp['Daily Store Sales'], color='blue')

plt.show()


