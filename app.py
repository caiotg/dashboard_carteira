import dash_bootstrap_components as dbc
import pandas as pd
import dash
from dash import Dash, html, dcc, dash_table, callback
from dash.dependencies import Input, Output
from carteira import Carteira

app = dash.Dash(
    external_stylesheets=[dbc.themes.SLATE]
)