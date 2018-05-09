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
df = pd.read_csv('names-all=years.csv')
df.head()
