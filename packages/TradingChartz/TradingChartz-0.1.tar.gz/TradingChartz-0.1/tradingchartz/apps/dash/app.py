# external standard
import datetime as dt

# external dash
import dash
import dash_bootstrap_components as dbc

# internal imports
import tradingchartz.apps.dash.dash_components.layout as ly
from tradingchartz.apps.dash.dash_components.callbacks import register_main_page_callbacks

app = dash.Dash(external_stylesheets=[dbc.themes.SUPERHERO])

app.layout = ly.layout

register_main_page_callbacks(app)

server = app.server

