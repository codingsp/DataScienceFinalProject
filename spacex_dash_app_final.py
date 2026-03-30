# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create dropdown options
unique_launch_sites = spacex_df['Launch Site'].unique().tolist()

launch_sites = []
launch_sites.append({'label': 'All Sites', 'value': 'All Sites'})

for site in unique_launch_sites:
    launch_sites.append({'label': site, 'value': site})

# Create slider marks
marks_dict = {}

for i in range(0, 11000, 1000):
    marks_dict[i] = {'label': str(i) + ' Kg'}

# Create Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div(children=[

    html.H1(
        'SpaceX Launch Records Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 40
        }
    ),

    # Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=launch_sites,
        value='All Sites',
        placeholder='Select a Launch Site',
        searchable=True
    ),

    html.Br(),

    html.Div(
        dcc.Graph(id='success-pie-chart')
    ),

    html.Br(),

    html.P("Payload range (Kg):"),

    dcc.RangeSlider(
        id='payload_slider',   # FIXED ID
        min=0,
        max=10000,
        step=1000,
        marks=marks_dict,
        value=[min_payload, max_payload]
    ),

    html.Div(
        dcc.Graph(id='success-payload-scatter-chart')
    )

])


# PIE CHART CALLBACK
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)

def get_pie_chart(entered_site):

    if entered_site == 'All Sites':

        data = spacex_df[
            spacex_df['class'] == 1
        ]

        fig = px.pie(
            data,
            names='Launch Site',
            title='Total Success Launches by Site'
        )

    else:

        data = spacex_df[
            spacex_df['Launch Site'] == entered_site
        ]

        fig = px.pie(
            data,
            names='class',
            title='Success vs Failure for site ' + entered_site
        )

    return fig



# SCATTER CALLBACK
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload_slider', 'value')   # FIXED ID
    ]
)

def get_scatter_chart(entered_site, payload_slider):

    low, high = payload_slider

    # Filter payload range
    data = spacex_df[
        spacex_df['Payload Mass (kg)'].between(low, high)
    ]

    # Filter by site
    if entered_site != 'All Sites':

        data = data[
            data['Launch Site'] == entered_site
        ]

        title_text = (
            'Correlation between Payload and Success for site ' + entered_site
        )

    else:

        title_text = (
            'Correlation between Payload and Success for all Sites'
        )

    fig = px.scatter(
        data,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',   # IMPORTANT FIX
        title=title_text
    )

    return fig


# Run app
if __name__ == '__main__':
    app.run(debug=True)