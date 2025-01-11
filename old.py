from dash import Dash, html, dcc, callback, Output, Input, dash_table,dcc
import plotly.express as px
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt



##campers
monthData['Region'] = monthData['Region'].str.strip()
## 

#plug and recieve data per region base, ignore initial variable names
southeast = monthData[monthData['Region']=='Pacific West'] 

campersSE = southeast['RecreationVisits']
yearAll = southeast['Year']

year = southeast['Year'].drop_duplicates(keep='first')
year = year.sort_values(

)

year = year.dropna()




##need averages per year


southeast_df = pd.DataFrame(campersSE.values, index=yearAll, columns=['RecreationVisits'])

avg_by_year = southeast_df.groupby('Year').mean()



avg_df = pd.DataFrame({'Year' : [year],'RecreationVisits' : [avg_by_year]} )