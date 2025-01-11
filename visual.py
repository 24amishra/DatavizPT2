from dash import Dash, html, dcc, callback, Output, Input, dash_table,dcc
import plotly.express as px
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt



import numpy as np

yearData = pd.read_csv('/Users/agastyamishra/Downloads/US-National-Parks_RecreationVisits_1979-2023.csv')

monthData = pd.read_csv('/Users/agastyamishra/Downloads/US-National-Parks_Use_1979-2023_By-Month.csv')
intermountain = yearData[yearData['Region']=='Intermountain']
intermountain = intermountain.groupby(['ParkName'],as_index=False).sum()
print(intermountain)


#  aggregate data so only one category(total vis) is visible for each year
yearData = yearData.groupby(['Year', 'Region'], as_index=False).sum()

""" app = Dash()







app.layout = [
    html.Div(children='Total Recreation Visits by Region'),
    dcc.Graph(figure=px.line(yearData, x='Year', y='RecreationVisits', color = 'Region'))
]


#run file 
if __name__ == '__main__':
    app.run(debug=True)
 """