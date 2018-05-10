import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
# import dash_table_experiments as dt
import pandas as pd
import numpy as np
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
    html.H3("Gender"),
    dcc.RadioItems(id='gender-select',
        options=[
            {'label': 'Female', 'value': 'F'},
            {'label': 'Male', 'value': 'M'},
            {'label': 'Either', 'value': 'E'}
        ],
        value='F'
    ),
    html.H3("Year Range"),
    html.Div(id='output-container-range-slider'),
    dcc.RangeSlider(id = 'popular-names-slider',
        marks={i: i for i in range(1880,2016,10)},
        min=1880,
        max=2016,
        value=[2000,2016]
    ),

    dcc.Graph(id='popular-graph'),
    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),

])

@app.callback(Output('popular-graph', 'figure'),
              [Input('popular-names-slider', 'value'),
               Input('gender-select', 'value')])
def popularGraph(yearRange, gender):
    filteredDf = df[(df.Year >= yearRange[0]) & (df.Year <= yearRange[1]) & (df.Gender == 'M')].groupby(['Name', 'Gender'],as_index = False)[['n']].sum().sort_values(["n"], ascending=False).iloc[:10,]

    girlsDf = df[(df.Year >= yearRange[0]) & (df.Year <= yearRange[1]) & (df.Gender == 'F')].groupby(['Name', 'Gender'], as_index = False)[['n']].sum().sort_values(["n"], ascending=False).iloc[:10,]
    if gender == 'E':
        filteredDf = pd.concat([filteredDf, girlsDf])
    print(filteredDf.head())
    traces = [go.Bar(
                x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                   2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                   350, 430, 474, 526, 488, 537, 500, 439],
                name='Rest of world',
                marker=go.Marker(
                    color='rgb(55, 83, 109)'
                )
            ),
            go.Bar(
                x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                   2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                   299, 340, 403, 549, 499],
                name='China',
                marker=go.Marker(
                    color='rgb(26, 118, 255)'
                )
            )
        ]
#    for i in filteredDf.Name:
#        df_by_continent = filtered_df[filtered_df['continent'] == i]
#        traces.append(go.Bar(
#            x=['giraffes', 'orangutans', 'monkeys'],
#            y=[20, 14, 23]
#        ))

    return {
        'data': traces,
        'layout': go.Layout(
            title='US Export of Plastic Scrap',
            showlegend=True,
            legend=go.Legend(
                x=0,
                y=1.0
            ),
            margin=go.Margin(l=40, r=0, t=40, b=30)
        )
    }


@app.callback(Output('output-container-range-slider', 'children'),
              [Input('popular-names-slider', 'value')])
def page_1_slider(value):
    return 'Year range {}-{}'.format(value[0], value[1])


page_2_layout = html.Div([
    html.H1('Page 2'),
    dcc.RadioItems(
        id='page-2-radios',
        options=[{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
        value='Orange'
    ),
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

@app.callback(Output('page-2-content', 'children'),
              [Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


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
