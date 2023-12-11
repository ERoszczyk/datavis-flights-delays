import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st
from streamlit_plotly_events import plotly_events

scale = [[0.0, 'rgb(0,100,0)'], [0.2, 'rgb(34,139,34)'],
         [0.4, 'rgb(60,179,60)'], [0.6, 'rgb(173,255,47)'],
         [0.8, 'rgb(255,215,0)'], [1.0, 'rgb(255,99,71)']]


def draw_map_with_mean_delay(df, start_date, end_date, start_time, end_time):
    df = df[(df['DATE'] >= start_date) & (df['DATE'] <= end_date) & (
            pd.to_datetime(df['ARRIVAL_TIME']).dt.time >= start_time) & (
                    pd.to_datetime(df['ARRIVAL_TIME']).dt.time <= end_time)]
    trace = go.Scattergeo(
        lon=df['LONGITUDE_x'],
        lat=df['LATITUDE_x'],
        text=('Airport: ' + df['AIRPORT_x'] + '<br>'
              + 'City: ' + df['CITY_x'] + '<br>'
              + 'State: ' + df['STATE_x'] + '<br>'
              + 'Percentage of delayed flights: '
              + (df['Percentage Delayed'].astype(float).round(2)).astype(str) + '%<br>'),
        mode='markers',
        marker=dict(
            autocolorscale=False,
            cmax=df['Percentage Delayed'].astype(float).max(),
            cmin=0,
            color=df['Percentage Delayed'],
            colorbar=dict(title="Percentage of Delay (%)"),
            colorscale=px.colors.sequential.YlOrRd,
            line=dict(
                color="rgba(102,102,102)",
                width=1
            ),
            opacity=0.8,
            size=8
        )
    )

    layout = go.Layout(
        showlegend=False,
        geo=dict(scope='north america',
                 projection=dict(type='natural earth'),
                 showlakes=True,
                 showland=True,
                 lakecolor='rgb(95,145,237)',
                 landcolor='rgb(250,250,250)',
                 ),
        margin=go.layout.Margin(
            l=20,
            r=20,
            b=30,
            t=20,
            pad=30
        ),
        autosize=True
    )

    fig = go.Figure(data=[trace], layout=layout)
    selected_airport = plotly_events(fig)
    if selected_airport:
        nr = selected_airport[0]['pointIndex']
        airport = df.iloc[nr]['AIRPORT_x']
        st.session_state.selected_airport = airport

def draw_routes(df, departure_cities, arrival_cities, departure_airports, arrival_airports):
    if len(departure_cities) > 0:
        df = df[df['CITY_x'].isin(departure_cities)]
    if len(arrival_cities) > 0:
        df = df[df['CITY_y'].isin(arrival_cities)]
    if len(departure_airports) > 0:
        df = df[df['AIRPORT_x'].isin(departure_airports)]
    if len(arrival_airports) > 0:
        df = df[df['AIRPORT_y'].isin(arrival_airports)]

    # draw the airport points in the map
    data = [dict(type='scattergeo',
                 lat=df['LATITUDE_x'],
                 lon=df['LONGITUDE_x'],
                 marker=dict(
                     color='#FFD700',
                     line=dict(
                         color="rgba(102,102,102)",
                         width=1
                     ),
                     opacity=0.8,
                     size=6,
                 ),
                 mode='markers',
                 name='',
                 )]
    data += [dict(type='scattergeo',
                  lat=df['LATITUDE_y'],
                  lon=df['LONGITUDE_y'],
                  marker=dict(
                      color='#FFD700',
                      line=dict(
                          color="rgba(102,102,102)",
                          width=1
                      ),
                      opacity=0.8,
                      size=6,
                  ),
                  mode='markers',
                  name='',
                  )]

    # draw the flight route in the map
    for i in range(df.shape[0]):
        data += [dict(
            lat=[df['LATITUDE_x'][i], df['LATITUDE_y'][i]],
            line=dict(
                color='#4682B4',
                width=1
            ),
            lon=[df['LONGITUDE_x'][i], df['LONGITUDE_y'][i]],
            mode="lines",
            text=('From: ' + (df['AIRPORT_x'][i])
                  + '<br>To: ' + df['AIRPORT_y'][i]
                  + '<br>Avg. Delay: '
                  + ((df['ARRIVAL_DELAY'][i] * 100).astype(int) / 100).astype(str)
                  + ' mins'
                  ),
            opacity=0.8,
            name='',
            type="scattergeo"
        )]

    # layout
    layout = go.Layout(geo=dict(scope='north america',
                                projection=dict(type="azimuthal equal area"),
                                showlakes=True,
                                showland=True,
                                lakecolor='rgb(95,145,237)',
                                landcolor='rgb(250,250,250)'
                                ),
                       margin=go.layout.Margin(
                           l=20,
                           r=80,
                           b=30,
                           t=20,
                           pad=30
                       ),
                       autosize=True,
                       showlegend=False
                       )

    fig = go.Figure(data=data, layout=layout)

    selected_route = plotly_events(fig)
    if selected_route:
        nr = selected_route[0]['curveNumber']

        airport_dep = df.iloc[nr - 2]['AIRPORT_x']
        airport_arr = df.iloc[nr - 2]['AIRPORT_y']
        st.session_state.route_origin = airport_dep
        st.session_state.route_destination = airport_arr
