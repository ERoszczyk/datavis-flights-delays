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


def route(flight, airport):
    # for origin airports info
    a = flight.loc[:, ['ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'ARRIVAL_DELAY']]
    a['AtoB'] = a['ORIGIN_AIRPORT'] + a['DESTINATION_AIRPORT']
    b = a.loc[:, ['AtoB', 'ARRIVAL_DELAY']].groupby('AtoB').mean()
    b['IATA_CODE'] = b.index.str[:3]
    c = pd.merge(airport, b.reset_index())
    c.rename(columns={'IATA_CODE': 'ORIGIN_AIRPORT'}, inplace=True)
    c_sorted = c.set_index('AtoB').sort_index()

    # for destination airports info
    b.drop('IATA_CODE', axis=1, inplace=True)
    b['IATA_CODE'] = b.index.str[3:]
    d = pd.merge(airport, b.reset_index())
    d.rename(columns={'IATA_CODE': 'DESTINATION_AIRPORT'}, inplace=True)
    d_sorted = d.set_index('AtoB').sort_index()

    return (c_sorted, d_sorted)


def draw_routes(df, airport_df, departure_cities, arrival_cities, departure_airports, arrival_airports):
    if len(departure_cities) > 0:
        df = df[df['CITY_x'].isin(departure_cities)]
    if len(arrival_cities) > 0:
        df = df[df['CITY_y'].isin(arrival_cities)]
    if len(departure_airports) > 0:
        df = df[df['AIRPORT_x'].isin(departure_airports)]
    if len(arrival_airports) > 0:
        df = df[df['AIRPORT_y'].isin(arrival_airports)]

    route_origin, route_destination = route(df, airport_df)

    # draw the airport points in the map
    data = [dict(type='scattergeo',
                 lat=route_origin['LATITUDE'],
                 lon=route_origin['LONGITUDE'],
                 marker=dict(
                     color='#FFD700',
                     line=dict(
                         color="rgba(102,102,102)",
                         width=1
                     ),
                     opacity=0.8,
                     size=6
                 ),
                 mode='markers',
                 )]
    data += [dict(type='scattergeo',
                  lat=route_destination['LATITUDE'],
                  lon=route_destination['LONGITUDE'],
                  marker=dict(
                      color='#FFD700',
                      line=dict(
                          color="rgba(102,102,102)",
                          width=1
                      ),
                      opacity=0.8,
                      size=6
                  ),
                  mode='markers',
                  )]

    # draw the flight route in the map
    for i in range(route_origin.shape[0]):
        data += [dict(
            lat=[route_origin['LATITUDE'][i], route_destination['LATITUDE'][i]],
            line=dict(
                color='#4682B4',
                width=1
            ),
            lon=[route_origin['LONGITUDE'][i], route_destination['LONGITUDE'][i]],
            mode="lines",
            text=('From: ' + (route_origin['AIRPORT'][i])
                  + '<br>To: ' + route_destination['AIRPORT'][i]
                  + '<br>Avg. Delay: '
                  + ((route_origin['ARRIVAL_DELAY'][i] * 100).astype(int) / 100).astype(str)
                  + ' mins'
                  ),
            opacity=0.8,
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

        airport_dep = route_origin.iloc[nr - 2]['AIRPORT']
        airport_arr = route_destination.iloc[nr - 2]['AIRPORT']
        st.session_state.route_origin = airport_dep
        st.session_state.route_destination = airport_arr
