import calendar
from datetime import time

import pandas as pd
import streamlit as st

MIN_MAX_RANGE = (time(0, 0), time(23, 59))
PRE_SELECTED_DATES = (time(0, 0), time(23, 59))


def display_time_filters():
    start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2015-01-01", format="%Y-%m-%d"),
                                       min_value=(pd.to_datetime("2015-01-01", format="%Y-%m-%d")),
                                       max_value=pd.to_datetime("2015-12-31", format="%Y-%m-%d"), key='start_date')
    end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2015-12-31", format="%Y-%m-%d"),
                                     min_value=start_date or pd.to_datetime("2015-01-01", format="%Y-%m-%d"),
                                     max_value=pd.to_datetime("2015-12-31", format="%Y-%m-%d"), key='end_date')

    min_time, max_time = st.sidebar.slider(
        "Departure time",
        value=PRE_SELECTED_DATES,
        min_value=MIN_MAX_RANGE[0],
        max_value=MIN_MAX_RANGE[1],
        key='time'
    )

    # convert the dates to string
    start = start_date.strftime("%Y-%m-%d")
    end = end_date.strftime("%Y-%m-%d")
    return start, end, min_time, max_time


def display_city_filter(df):
    dep_city_list = list(df['CITY_x'].unique())
    arr_city_list = list(df['CITY_y'].unique())
    dep_city_list.sort()
    arr_city_list.sort()
    return st.sidebar.multiselect('Departure city', dep_city_list, key='dep_city'), st.sidebar.multiselect(
        'Arrival city',
        arr_city_list, key='arr_city')


def display_airport_filter(df, departure_cities, arrival_cities):
    dep_airport_list = list(df['AIRPORT_x'].unique())
    if len(departure_cities) > 0:
        dep_airport_list = list(df[df['CITY_x'].isin(departure_cities)]['AIRPORT_x'].unique())
    arr_airport_list = list(df['AIRPORT_y'].unique())
    if len(arrival_cities) > 0:
        arr_airport_list = list(df[df['CITY_y'].isin(arrival_cities)]['AIRPORT_y'].unique())
    dep_airport_list.sort()
    arr_airport_list.sort()
    return st.sidebar.multiselect('Departure airport', dep_airport_list, key='dep_airport'), st.sidebar.multiselect(
        'Arrival airport', arr_airport_list, key='arr_airport')


def display_airline_filter(df):
    airline_list = list(df['AIRLINE'].unique())
    airline_list.sort()
    airline_list = ['All'] + airline_list
    return st.sidebar.selectbox('Airline', airline_list, key='airline')


def display_airlines_filter(df):
    airline_list = list(df['AIRLINE'].unique())
    airline_list.sort()
    return st.sidebar.multiselect('Airline', airline_list, key='airlines')


def display_month_filter():
    # Specify the order of months
    months_order = list(calendar.month_name)[1:]
    months_order = ['All'] + months_order
    return st.sidebar.selectbox('Month', months_order, key='month_selector')


def display_type_filter():
    return st.sidebar.radio('Type', ['All', 'On Time', 'Delayed', 'Cancelled'], key='type')


def display_timeonly_filter():
    min_time, max_time = st.sidebar.slider(
        "Departure time",
        value=PRE_SELECTED_DATES,
        min_value=MIN_MAX_RANGE[0],
        max_value=MIN_MAX_RANGE[1],
        key='time'
    )

    return min_time, max_time
