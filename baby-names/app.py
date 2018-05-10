import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
# import dash_table_experiments as dt
import pandas as pd
import numpy as np
from random import randint
import plotly.graph_objs as go
from flask import send_from_directory
import os

app = dash.Dash(__name__, static_folder='static')
server = app.server
app.title = "Baby Name Analyzer"
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
#df= pd.read_csv('http://files.zillowstatic.com/research/public/Zip/Zip_MedianValuePerSqft_AllHomes.csv')
df = pd.read_csv('names-all-years.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)
uniqueNames = df.Name.unique()
namesOptions = [{'label':n, 'value': n} for n in sorted(uniqueNames)]



app = dash.Dash()

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    dcc.Link('Popular Names', href='/popular'),
    html.Br(),
    dcc.Link('Names Over Time', href='/time'),
])

page_1_layout = html.Div([
    html.H1('Popular Names'),
    dcc.Link('Names Over Time', href='/time'),
    dcc.Link('Home', href='/'),
    html.H3("Gender"),
    dcc.RadioItems(id='gender-select',
        options=[
            {'label': 'Female', 'value': 'F'},
            {'label': 'Male', 'value': 'M'},
            {'label': 'Both', 'value': 'E'}
        ],
        value='F'
    ),
    html.H3("Year Range"),
    html.H4(id='output-container-range-slider'),
    dcc.RangeSlider(id = 'popular-names-slider',
        marks={i:"{}".format(i) for i in range(1880,2016,10)},
        min=1880,
        max=2016,
        value=[2000,2016],

    ),
    dcc.Graph(id='popular-graph'),


])

@app.callback(Output('popular-graph', 'figure'),
              [Input('popular-names-slider', 'value'),
               Input('gender-select', 'value')])
def popularGraph(yearRange, gender):
    filteredDf = df[(df.Year >= yearRange[0]) & (df.Year <= yearRange[1]) & (df.Gender == 'M')].groupby(['Name', 'Gender'],as_index = False)[['n']].sum().sort_values(["n"], ascending=False).iloc[:10,]
    girlsDf = df[(df.Year >= yearRange[0]) & (df.Year <= yearRange[1]) & (df.Gender == 'F')].groupby(['Name', 'Gender'], as_index = False)[['n']].sum().sort_values(["n"], ascending=False).iloc[:10,]
    babyBlue = ['rgb(137, 207, 240)']*10
    babyPink = ['rgb(244, 194, 194)']*10
    myColors = babyBlue
    if gender == 'E':
        filteredDf = pd.concat([filteredDf, girlsDf])
        myColors.extend(babyPink)
    elif gender == 'F':
        filteredDf = girlsDf
        myColors = babyPink

    traces = [go.Bar(
                x=filteredDf.Name,
                y=filteredDf.n,
                name= 'Total Count',
                marker=go.Marker(
                    color=myColors

                )
            )
        ]
    return {
        'data': traces,
        'layout': go.Layout(
            title='Popular US Names',
            margin=go.Margin(l=40, r=40, t=40, b=40)
        )
    }
@app.callback(Output('output-container-range-slider', 'children'),
              [Input('popular-names-slider', 'value')])
def page_1_slider(value):
    return '{}-{}'.format(value[0], value[1])


page_2_layout = html.Div([
    html.H1('Names Over Time'),
    dcc.Link('Popular Names', href='/popular'),
    dcc.Link('Home', href='/'),
    html.H3("Gender"),
    dcc.RadioItems(id='gender-select',
        options=[
            {'label': 'Female', 'value': 'F'},
            {'label': 'Male', 'value': 'M'},
            {'label': 'Both', 'value': 'E'}
        ],
        value='E'
    ),
    dcc.Dropdown(id="name-select",
        options=namesOptions,
        value=namesOptions[randint(0,len(namesOptions)-1)].get('value')
    ),
    # html.H3("Year Range"),
    # html.H4(id='output-container-range-slider'),
    # dcc.RangeSlider(id = 'popular-names-slider',
    #     marks={i:"{}".format(i) for i in range(1880,2016,10)},
    #     min=1880,
    #     max=2016,
    #     value=[1880,2016],
    #
    # ),

    dcc.Graph(id='time-graph'),
])
@app.callback(Output('time-graph', 'figure'),
              [Input('name-select', 'value'),
              Input('gender-select', 'value')
               ])
def popularGraph(name, gender):
    filteredDf = df[(df.Name == name)]
    if gender != 'E':
        filteredDf = filteredDf[(filteredDf.Gender == gender)]
    traces = []
    for i in filteredDf.Gender.unique():
        curDf = filteredDf[filteredDf.Gender == i]
        traces.append(go.Scatter(
                    x=curDf.Year,
                    y=curDf.n,
                    mode='lines+markers',
                    name=i
                ))
    # traces = [go.Scatter(
    #             x=filteredDf.Year,
    #             y=filteredDf.n,
    #             mode='lines+markers'
    #         )
    #     ]
    return {
        'data': traces,
        'layout': go.Layout(
            title='Names Over Time',
            margin=go.Margin(l=40, r=40, t=40, b=40)
        )
    }


# Update the index
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/popular':
        return page_1_layout
    elif pathname == '/time':
        return page_2_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here

#app.css.append_css({
#    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
#})


if __name__ == '__main__':
    app.run_server(debug=True)
