import datetime

import pandas as pd
import streamlit as st

from draw_map import draw_routes
from draw_statistics import draw_avg_flight_delay_by_delay_type_routes, \
    draw_monthly_avg_flight_delay_by_month_routes
from filters import display_time_filters, display_city_filter, display_airport_filter

PAGE_TITLE = 'Flight Delays'
PAGE_ICON = '🗺️'
APP_SUB_TITLE = 'Data Visualisation 2023'
SIDEBAR_TITLE = 'Filter data'


def set_streamlit_page():
    st.set_page_config(PAGE_TITLE, layout="wide", page_icon=PAGE_ICON)
    st.title("Average flight delays by routes 2015")
    st.sidebar.title(SIDEBAR_TITLE)
    st.markdown("""
      <style>
        .st-emotion-cache-16txtl3 {
          margin-top: -75px;
        }
      </style>
    """, unsafe_allow_html=True)


def reset_filters():
    st.session_state.start_date = pd.to_datetime("2015-01-01", format="%Y-%m-%d")
    st.session_state.end_date = pd.to_datetime("2015-12-31", format="%Y-%m-%d")
    st.session_state.time = (datetime.time(0, 0), datetime.time(23, 59))
    st.session_state.arr_city = []
    st.session_state.dep_city = []
    st.session_state.dep_airport = []
    st.session_state.arr_airport = []


def main():
    df = pd.read_csv('2015_dataset/merged_1k_sample.csv')
    start, end, min_time, max_time = display_time_filters()
    dep_cities, arr_cities = display_city_filter(df)
    dep_airport, arr_airport = display_airport_filter(df, dep_cities, arr_cities)
    st.sidebar.button('Reset filters', on_click=reset_filters)
    draw_routes(df, dep_cities, arr_cities, dep_airport, arr_airport)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Reset"):
            st.session_state.route_origin = None
            st.session_state.route_destination = None
    with col2:
        if 'route_origin' in st.session_state and st.session_state.route_origin:
            st.text("Selected route: {} - {}".format(st.session_state.route_origin, st.session_state.route_destination))
        else:
            "Route not selected"
    with col1:
        draw_avg_flight_delay_by_delay_type_routes(df,
                                                   st.session_state.route_origin if 'route_origin' in st.session_state else None,
                                                   st.session_state.route_destination if 'route_destination' in st.session_state else None,
                                                   start, end, min_time, max_time)
    with col2:
        draw_monthly_avg_flight_delay_by_month_routes(df,
                                                      st.session_state.route_origin if 'route_origin' in st.session_state else None,
                                                      st.session_state.route_destination if 'route_destination' in st.session_state else None,
                                                      start, end, min_time, max_time)


if __name__ == "__main__":
    set_streamlit_page()
    main()
