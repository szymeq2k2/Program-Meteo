import requests
import matplotlib.pyplot as plt
import json
import dash_html_components as html
import pandas as pd
import webbrowser
import datetime
import plotly.express as px
import dash_core_components as dcc
import numpy as np
import re
import dash


request_for = requests.get("http://api.openweathermap.org/data/2.5/forecast?lat=50.040003&lon=18.394399&APPID=7cf51f9cd2de7b8e469a6e0ea1bf986c&units=metric")
for_weather = request_for.content.strip()
json_data_for = json.loads(for_weather)


request_loc = requests.get("http://api.openweathermap.org/data/2.5/weather?lat=50.040003&lon=18.394399&APPID=7cf51f9cd2de7b8e469a6e0ea1bf986c&units=metric")
loc_weather = request_loc.content.strip()
json_data = json.loads(loc_weather)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


data = {'temp': json_data['main']['temp'], 'feels like': json_data['main']['feels_like'], 'temp min': json_data['main']['temp_min'], 'temp max':json_data['main']['temp_max'] }
names = list(data.keys())
values = list(data.values())
df1 = pd.DataFrame({"x": names,"y": values})
fig1 = px.bar(df1, x="x",y="y" ,barmode="group")

values=[json_data['wind']['speed'],json_data['wind']['speed']]
names = ["speed","gust"]
df2 =pd.DataFrame({"x":names,"y":values})
fig2 = px.bar(df2,x="x",y="y",barmode="group")

values=[json_data['main']['humidity']]
names=["humidity"]
df3 =pd.DataFrame({"x":names,"y":values})
fig3 = px.bar(df3,x="x",y="y",barmode="group")

values=[json_data_for['list'][0]['main']['temp'],json_data_for['list'][1]['main']['temp'],json_data_for['list'][2]['main']['temp'],json_data_for['list'][3]['main']['temp'],json_data_for['list'][4]['main']['temp']]
names=[1,2,3,4,5]
df4 =pd.DataFrame({"x":names,"y":values})
fig4 = px.line(df4,x="x",y="y")

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(children=[

    html.H1(
    children='Temperature today ',
    style={
        'textAlign': 'center',
        'color': colors['text']
    }
    ),

    dcc.Graph(
        id='temp',
        figure=fig1
    ),

    html.H1(
    children='Wind today ',
    style={
        'textAlign': 'center',
        'color': colors['text']
    }
    ),

    dcc.Graph(
        id='wind',
        figure=fig2
    ),

    html.H1(
    children='Humid today ',
    style={
        'textAlign': 'center',
        'color': colors['text']
    }
    ),

    dcc.Graph(
        id='humid',
        figure=fig3
    ),

    html.H1(
    children='Temperature in future ',
    style={
        'textAlign': 'center',
        'color': colors['text']
    }
    ),

    dcc.Graph(
        id='future',
        figure=fig4
    )

])

