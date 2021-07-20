import dash  # Dash 1.16 or higher
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pathlib
import pandas as pd
import plotly.express as px
from app import app
# need to pip install statsmodels for trendline='ols' in scatter plot

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

# Data from U.S. Congress, Joint Economic Committee, Social Capital Project. https://www.jec.senate.gov/public/index.cfm/republicans/2018/4/the-geography-of-social-capital-in-america
df = pd.read_csv(r"C:\Users\User\Downloads\Update-Rani 14.csv")

static_graph = dcc.Graph(
        id='example-graph',
        figure={}
    )
layout = html.Div([
    html.Label("Block/Municipality", style={'fontSize':30, 'textAlign':'center'}),
    dcc.Dropdown(
        id='states-dpdn',
        options=[{'label': s, 'value': s} for s in sorted(df.Places.unique())],
        value=None,
        clearable=False
    ),
    html.Label("Petitions", style={'fontSize':30, 'textAlign':'center'}),
    dcc.Dropdown(id='counties-dpdn',
                 options=[],
                 value=[],
                 multi=True),
    dcc.Loading([static_graph]),
    html.Br(),
])
# Populate the counties dropdown with options and values
@app.callback(
    Output('counties-dpdn', 'options'),
    Output('counties-dpdn', 'value'),
    Input('states-dpdn', 'value'),
)
def set_cities_options(chosen_state):
    dff = df[df.Places==chosen_state]
    counties_of_states = [{'label': c, 'value': c} for c in sorted(dff.Locations.unique())]
    values_selected = [x['value'] for x in counties_of_states]
    return counties_of_states, values_selected


# Create graph component and populate with scatter plot
@app.callback(
    Output('example-graph', 'figure'),
    Input('counties-dpdn', 'value'),
    Input('states-dpdn', 'value'),
    prevent_initial_call=True
)
def update_grpah(selected_counties, selected_state):
    if len(selected_counties) == 0:
        return dash.no_update
    else:
        dff = df[(df.Places==selected_state) & (df.Locations.isin(selected_counties))]

    fig = px.histogram(df, x='Issues', y='Percentage', color = 'TotalPetitions', barmode="group")
    return fig
