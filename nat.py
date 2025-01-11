import pandas as pd
import matplotlib.pyplot as plt



import numpy as np

yearData = pd.read_csv('/Users/agastyamishra/Downloads/US-National-Parks_RecreationVisits_1979-2023.csv')

monthData = pd.read_csv('/Users/agastyamishra/Downloads/US-National-Parks_Use_1979-2023_By-Month.csv')


#  test to see tent/rv numbers for zion NP

##campers
monthData['Region'] = monthData['Region'].str.strip()
## this code can be altered by changing the value on the right side of the equals

#plug and recieve data per region base, ignore initial variable names
southeast = monthData[monthData['Region']=='Pacific West'] 

campersSE = southeast['RecreationVisits']
yearAll = southeast['Year']

year = southeast['Year'].drop_duplicates(keep='first')
year = year.sort_values(

)

year = year.dropna()

#print(campersSE)


##need averages per year
#campersSE.plot()
#plt.show()
southeast_df = pd.DataFrame(campersSE.values, index=yearAll, columns=['RecreationVisits'])

avg_by_year = southeast_df.groupby('Year').mean()



avg_df = pd.DataFrame(avg_by_year,index=year, columns = ['RecreationVisits'])


avg_df.plot()
plt.xlabel('Year')
plt.ylabel('Number of Recreation Visits')

plt.title("Number of Recreation Visits in the Pacific West NP Region from 1979-2023")

plt.show()










#plt.show()


##print(rvRegion)













