from dash import Dash, html, dcc, callback, Output, Input, dash_table,dcc
import plotly.express as px
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt



import numpy as np

yearData = pd.read_csv('/Users/agastyamishra/Downloads/US-National-Parks_RecreationVisits_1979-2023.csv')

monthData = pd.read_csv('/Users/agastyamishra/Downloads/US-National-Parks_Use_1979-2023_By-Month.csv')
#intermountain = yearData[yearData['Region']=='Intermountain']
#intermountain = intermountain.groupby(['ParkName'],as_index=False).sum()
















#average of all the data in monthData per year
monthData = monthData.groupby(['Year','Region'],as_index=False).sum()


#  aggregate data so only one category(total vis) is visible for each year
yearData = yearData.groupby(['Year', 'Region'], as_index=False).sum()
app = Dash()







app.layout = html.Div([
       
    
    html.Div(children='An interdisciplinary analysis of the National Parks System'),
    dcc.Graph(figure=px.line(yearData, x='Year', y='RecreationVisits', color = 'Region')),
    dcc.Graph(figure = px.line(monthData, x = 'Year', y = 'TentCampers', color = 'Region' )),

    html.Div([
            dcc.Dropdown(
                
                'Number of RV Campers',
                id='crossfilter-yaxis-column'
            ),
])

])










"""  @callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-yaxis-column', 'value'),
    Input('crossfilter-xaxis-type', 'value'),
    Input('crossfilter-yaxis-type', 'value'),
    Input('crossfilter-year--slider', 'value')) """


#run file 
if __name__ == '__main__':
    app.run(debug=True)
