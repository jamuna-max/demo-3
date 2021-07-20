import plotly.express as px
import pandas as pd
import pathlib
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from app import app

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

dfv = pd.read_csv(r"C:\Users\User\Downloads\Ranipet_update.csv") # GregorySmith Kaggle
Locations = dfv.Locations.unique()
TotalPetitions = dfv.TotalPetitions.unique()
colors = {
    'background': '#9FEAD8'
}
layout = html.Div([
    html.H1('Ranipet Assembly Constituency ', style={"textAlign": "center"}),
    html.Div(style={'backgroundColor': colors['background']}),
    html.Div([
        html.Div(

            dcc.Dropdown(
            id='genre-dropdown', value='Strategy', clearable=False,
            options=[{'label': x, 'value': x} for x in (dfv.Locations.unique())]
        ), className='six columns'),

        html.Div(
            dcc.Dropdown(
            id='sales-dropdown', value='EU Sales', clearable=False,
            persistence=True, persistence_type='memory',
            options=[{'label': x, 'value': x} for x in TotalPetitions]
        ), className='six columns'),
    ], className='row'),

    dcc.Graph(id='my-bar', figure={
     'layout':{ 'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background']}})
])


@app.callback(
    Output(component_id='my-bar', component_property='figure'),
    [Input(component_id='genre-dropdown', component_property='value'),
     Input(component_id='sales-dropdown', component_property='value')]
)
def display_value(Locations, TotalPetitions):
    dfv_fltrd = dfv[(dfv.Locations == Locations)]
    dfv_fltrd =  dfv[(dfv.TotalPetitions == TotalPetitions)]
    fig = px.bar(dfv_fltrd, x='Places', y='Percentage', color='Issues')
    fig = fig.update_yaxes(tickprefix="%")
    return fig

