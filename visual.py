from dash import Dash, html, dcc, callback, Output, Input, dash_table,dcc
import plotly.express as px
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt



import numpy as np

yearData = pd.read_csv('/Users/agastyamishra/Downloads/US-National-Parks_RecreationVisits_1979-2023.csv')

monthData = pd.read_csv('/Users/agastyamishra/Downloads/US-National-Parks_Use_1979-2023_By-Month.csv', delimiter=',', quotechar='"', encoding='utf-8')

#intermountain = yearData[yearData['Region']=='Intermountain']
#intermountain = intermountain.groupby(['ParkName'],as_index=False).sum()
monthData['Region'] = monthData['Region'].str.strip()

intermountain = monthData[monthData['Region'] == 'Intermountain']
alaska = monthData[monthData['Region'] == 'Alaska']
midwest= monthData[monthData['Region'] == 'Midwest']
northeast = monthData[monthData['Region'] == 'Northeast']
pacwest = monthData[monthData['Region'] == 'Pacific West']
southeast = monthData[monthData['Region'] == 'Southeast']


regions = [intermountain, alaska,midwest,northeast,pacwest,southeast]

#average of all the data in monthData per year

for idx, region in enumerate(regions):
    regions[idx] = region.groupby(['Year', 'ParkName'], as_index=False).sum()




monthData = monthData.groupby(['Year','Region'],as_index=False).sum()



#  aggregate data so only one category(total vis) is visible for each year
yearData = yearData.groupby(['Year', 'Region'], as_index=False).sum()





app = Dash()





col = ['Backcountry','RVCampers','TentCampers']


app.layout = html.Div([
    
       
    
    html.Div(children='An interdisciplinary analysis of the National Parks System'),
    dcc.Graph(figure=px.line(yearData, x = 'Year', y='RecreationVisits', color = 'Region')),
    html.Div([
            dcc.Dropdown(
                 col,
                col[0],
                id='crossfilter-yaxis-column'
            ),
    dcc.Graph(figure = px.line(monthData, x = 'Year', y = 'TentCampers', color = 'Region' ,title = 'Total Recreation Visits to NP' ),id = 'crossfilter-indicator-line'),

    
    html.Div([
        dcc.Graph(figure = px.line(alaska,x = 'Year', y = 'RecreationVisits' , color = 'ParkName'))


    

    ]), html.Div([











    ])





])


])
@callback(
    Output('crossfilter-indicator-line', 'figure'),
    Input('crossfilter-yaxis-column', 'value'))

def update_graph( yaxis_column_name):


    
    figure = px.line(monthData, x = 'Year', y = yaxis_column_name, color = 'Region' )



    figure.update_yaxes(title=yaxis_column_name)
    return figure



#run file 
if __name__ == '__main__':
    app.run(debug=True)
