from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

yearData = pd.read_csv('/Users/agastyamishra/Downloads/US-National-Parks_RecreationVisits_1979-2023.csv')
monthData = pd.read_csv('/Users/agastyamishra/Downloads/US-National-Parks_Use_1979-2023_By-Month.csv', delimiter=',', quotechar='"', encoding='utf-8')

# Strip any spaces from region names
monthData['Region'] = monthData['Region'].str.strip()

# Split monthData into regions
regions = {
    'Intermountain': monthData[monthData['Region'] == 'Intermountain'],
    'Alaska': monthData[monthData['Region'] == 'Alaska'],
    'Midwest': monthData[monthData['Region'] == 'Midwest'],
    'Northeast': monthData[monthData['Region'] == 'Northeast'],
    'Pacific West': monthData[monthData['Region'] == 'Pacific West'],
    'Southeast': monthData[monthData['Region'] == 'Southeast']
}

# Group data by Year and Region
monthData_grouped = monthData.groupby(['Year', 'Region'], as_index=False).sum()

# Aggregate the yearData similarly
yearData = yearData.groupby(['Year', 'Region'], as_index=False).sum()

app = Dash()

col = ['Backcountry','RVCampers','TentCampers']

app.layout = html.Div([
    html.Div(children='An interdisciplinary analysis of the National Parks System'),
    dcc.Graph(
        figure=px.line(yearData, x='Year', y='RecreationVisits', color='Region'),
        id='crossfilter-indicator-line'
    ),
    dcc.Graph(
        figure=px.line(
            monthData_grouped,
            x='Year',
            y='TentCampers',
            color='Region',
            title='Total Recreation Visits to NP',
            
            
        ),id = 'crossfilter-yaxis'
    ),
    html.Div([
        dcc.Dropdown(
            options=[{'label': col_item, 'value': col_item} for col_item in col],
            value=col[0],
            id='crossfilter-yaxis-column'
        )
    ]),
    html.Div([
        dcc.Graph(id='hover-line-graph')
    ])
])

@callback(
    Output('hover-line-graph', 'figure'),
    Input('crossfilter-indicator-line', 'hoverData'),
   
   
)
def update_hover_line_graph(hoverData):
    # Check if hoverData is not None
    if hoverData is None:
        return px.line(title="Hover over a line to see details")

    # Extract the region (line) being hovered over
    curve_number = hoverData['points'][0]['curveNumber']  # Get curveNumber from hoverData

    # Get the corresponding Region name using curveNumber
    trace_regions = monthData_grouped['Region'].unique()
    
    # Ensure curveNumber is valid
    if curve_number < len(trace_regions):
        region_name = trace_regions[curve_number]
    else:
        return px.line(title="Invalid hover data")

    # Filter the data for the specific region
    filtered_data = monthData[monthData['Region'] == region_name]
    filtered_data = filtered_data.groupby(['Year', 'Region','ParkName'], as_index=False).sum(numeric_only=True)
    # Create a new graph for the hovered region
    fig = px.line(
        filtered_data,
        x='Year',
        y='RecreationVisits',
        title=f'Total Recreation Visitors in {region_name}',
        color='ParkName'  # Optional: Show parks within the region
    )

    return fig

@app.callback(
    Output('crossfilter-yaxis', 'figure'),
    Input('crossfilter-yaxis-column', 'value')
)
def update_graph(yaxis_column_name):
    figure = px.line(monthData_grouped, x='Year', y=yaxis_column_name, color='Region')
    figure.update_yaxes(title=yaxis_column_name)
    return figure

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
