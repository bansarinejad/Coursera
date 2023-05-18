# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True),
    html.Br(),

    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider', 
                    min=min_payload, 
                    max=max_payload, 
                    value=[min_payload, max_payload]),

    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    if option_slctd == 'ALL':
        fig = px.pie(spacex_df, names='Launch Site', 
                     title='Total Success Launches By Site')
    else:
        df = spacex_df[spacex_df['Launch Site'] == option_slctd]
        fig = px.pie(df, names='class', 
                     title=f'Total Success Launches for site {option_slctd}')

    return fig

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_plot(site_dropdown, payload_slider):
    if site_dropdown == 'ALL':
        fig = px.scatter(spacex_df, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category', range_y=[-0.5,1.5],
                         range_x=[payload_slider[0], payload_slider[1]])
    else:
        df = spacex_df[spacex_df['Launch Site'] == site_dropdown]
        fig = px.scatter(df, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category', range_y=[-0.5,1.5],
                         range_x=[payload_slider[0], payload_slider[1]])

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8090)
