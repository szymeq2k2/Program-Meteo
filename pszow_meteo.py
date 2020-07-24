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
from meteo_db import max_min_avg
from meteo_db import add_Data
from datetime import timedelta



# forecastData returns forecast data
def forecastData():
    request_for = requests.get("http://api.openweathermap.org/data/2.5/forecast?lat=50.040003&lon=18.394399&APPID=7cf51f9cd2de7b8e469a6e0ea1bf986c&units=metric")
    for_weather = request_for.content.strip()
    data_for = json.loads(for_weather)
    return data_for

# forecastData returns current data
def currentData():
    request_loc = requests.get("http://api.openweathermap.org/data/2.5/weather?lat=50.040003&lon=18.394399&APPID=7cf51f9cd2de7b8e469a6e0ea1bf986c&units=metric")
    loc_weather = request_loc.content.strip()
    data = json.loads(loc_weather)
    return data

#get_dates returns date after days_pass days passed 
def get_dates(days_pass):
    date_today = datetime.datetime.today()
    date1 = date_today + timedelta(days = days_pass)
    return date1.strftime('%A')

#creating_dash_board creates a dashboard
def creating_dash_board(json_data,json_data_for,dark):

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.css.append_css({'external_url': 'reset.css'})
    data = {'temp': json_data['main']['temp'], 'feels like': json_data['main']['feels_like'], 'temp min': json_data['main']['temp_min'], 'temp max':json_data['main']['temp_max'] }
    names = list(data.keys())
    values = list(data.values())
    df1 = pd.DataFrame({"Type": names,"°C": values})
    fig1_day = px.bar(df1, x="Type",y="°C" ,barmode="group")
    fig1_night = px.bar(df1, x="Type",y="°C" ,barmode="group",color_discrete_sequence =['darkblue']*3).update_layout({
                                    'paper_bgcolor': colors['background'],
                                    'plot_bgcolor': colors['graph-bg-dark']
                                    })

    wind_speed= str(json_data['wind']['speed'])+'km/h'
    wind_gust= str(json_data['wind']['speed'])+'km/h'
    humidity_value='Humidity level = '+str(json_data['main']['humidity'])+'%'

    values=[json_data_for['list'][1]['main']['temp'],json_data_for['list'][2]['main']['temp'],json_data_for['list'][3]['main']['temp'],json_data_for['list'][4]['main']['temp'],json_data_for['list'][5]['main']['temp']]
    names=[get_dates(1),get_dates(2),get_dates(3),get_dates(4),get_dates(5)]
    df4 =pd.DataFrame({"Day":names,"°C":values})
    fig4_day = px.line(df4,x="Day",y="°C")
    fig4_night = px.line(df4,x="Day",y="°C",color_discrete_sequence =['darkblue']*3).update_layout({
                                    'paper_bgcolor': colors['background'],
                                    'plot_bgcolor': colors['graph-bg-dark']
                                    })
                                    
    if dark==True:
        app.layout = create_dash_layout_night(fig1_night,fig4_night,wind_gust,wind_speed,humidity_value,app)
    else:
        app.layout = create_dash_layout_day(fig1_day,fig4_day,wind_gust,wind_speed,humidity_value,app)
    return app

#returns app with bright layout
def create_dash_layout_day(fig1,fig4,wind_gust,wind_speed,humidity_value,app):
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
        html.H2(
        children=wind_speed ,
            style={
            'textAlign': 'center'
            }
        
        ),
        html.H2(
        children=wind_gust ,
            style={
            'textAlign': 'center'
            }
        ),

        html.H1(
        children='Humid today ',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
        ),
        html.H2(
        children=humidity_value ,
            style={
            'textAlign': 'center'
            }
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
    return app.layout

#returns app with dark layout
def create_dash_layout_night(fig1,fig4,wind_gust,wind_speed,humidity_value,app):
    app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
        html.H1(
        children='Temperature today ',
        style={
            'textAlign': 'center',
            'color': colors['text-dark']
        }
        ),

        dcc.Graph(
            id='temp',
            figure=fig1 ,
        ),

        html.H1(
        children='Wind today ',
        style={
            'textAlign': 'center',
            'color': colors['text-dark']
        }
        ),
        html.Div(style={'backgroundColor': colors['tiles-color-night'] ,'height': 100 ,'width': 100},children=[
            html.H3(
            children=wind_speed ,
            style={
                'textAlign': 'center',
                'color': colors['text-dark']
            }
            )
        ]
        ),
        html.Div(style={'backgroundColor': colors['tiles-color-night']},children=[
            html.H2(
            children=wind_gust ,
            style={
                'textAlign': 'center',
                'color': colors['text-dark']
            }
            )
        ]
        
        ),

        html.H1(
        children='Humid today ',
        style={
            'textAlign': 'center',
            'color': colors['text-dark']
        }
        ),
        html.H2(
        children=humidity_value ,
        style={
            'textAlign': 'center',
            'color': colors['text-dark']
        }
        ),

        html.H1(
        children='Temperature in future ',
        style={
            'textAlign': 'center',
            'color': colors['text-dark']
        }
        ),

        dcc.Graph(
            id='future',
            figure=fig4 ,
        )
        
    ])
    return app.layout
#its a start funcion
def start():
    end=False
    print('In order to see all commands input "help"')
    while end == False:
        choice = input("Input: ")
        if choice == "help":
            print("\n"+"help - displays all commands."+"\n"+"temp - display min max temperature from selected day and avg temp from all data"+"\n"+"today - display values in console from today"+"\n"+"add - adds data from today to database"+"\n"+"show - shows data on diagrams "+"\n"+"quit - closes the aplication"+"\n")
        elif choice == "temp":
            print("Input date like this 2020-07-21-09:01")
            date = input()
            print(max_min_avg(date))
        # elif choice=="show":
                
        elif choice == "add":
            add_Data(weatherNow)
        elif choice == "show":
            if __name__ == '__main__':
                app=creating_dash_board(json_data,json_data_for,False)
                webbrowser.open('http://127.0.0.1:8050/')
                app.run_server()
        elif choice == "show -d":
            if __name__ == '__main__':
                app=creating_dash_board(json_data,json_data_for,True)
                webbrowser.open('http://127.0.0.1:8050/')
                app.run_server()
        elif choice == "today":
            print("temp = "+str(json_data['main']['temp'])+"\n"+"temp min = "+str(json_data['main']['temp_min'])+"\n"+"temp max = "+str(json_data['main']['temp_max'])+"\n"+"humidity = "+str(json_data['main']['humidity'])+"\n"+"wind = "+str(json_data['wind']['speed'])+"\n")
        elif choice == "quit":
            end=True

colors = {
    'background': '#1a1a1a',
    'text': '#7FDBFF',
    'text-dark': '#00EA64',
    'graph-bg-dark': '#6E6E6E',
    'tiles-color-day': '#a1acc2',
    'tiles-color-night': '#7f8899'
 }

x = datetime.datetime.today().strftime('%Y-%m-%d-%H:%M')
# print(x)
json_data = currentData()
json_data_for = forecastData()
avg =(json_data['main']['temp_min']+json_data['main']['temp_max'])/2
weatherNow =[(str(x),json_data['main']['temp'],avg,json_data['main']['temp_min'],json_data['main']['temp_max'],json_data['main']['humidity'],json_data['wind']['speed'])]

start()




