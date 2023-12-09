import datetime

import pandas as pd
import streamlit as st

from draw_statistics import draw_no_flights_by_month, draw_flight_no, number_of_flights_by_day_of_week
from filters import display_timeonly_filter, display_type_filter, display_airline_filter

PAGE_TITLE = 'Flight Delays'
PAGE_ICON = '📅'
APP_SUB_TITLE = 'Data Visualisation 2023'
SIDEBAR_TITLE = 'Filter data'


def set_streamlit_page():
    st.set_page_config(PAGE_TITLE, layout="wide", page_icon=PAGE_ICON)
    st.title("Average flight delays by time 2015")
    st.sidebar.title(SIDEBAR_TITLE)
    st.markdown("""
      <style>
        .st-emotion-cache-16txtl3 {
          margin-top: -75px;
        }
      </style>
    """, unsafe_allow_html=True)


def reset_filters():
    st.session_state.airline = 'All'
    st.session_state.time = (datetime.time(0, 0), datetime.time(23, 59))
    st.session_state.type = 'All'


def main():
    df = pd.read_csv('2015_dataset/merged_1k_sample.csv')
    airline_df = pd.read_csv('2015_dataset/airlines.csv')

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Reset", key='button1'):
            st.session_state.airline = 'All'
    with col2:
        if 'airline' in st.session_state and st.session_state.airline != 'All':
            st.text("Selected airline: {}".format(st.session_state.airline))
        else:
            "Airline not selected"

    airline = display_airline_filter(airline_df)
    start_time, end_time = display_timeonly_filter()
    type = display_type_filter()
    st.sidebar.button('Reset filters', on_click=reset_filters)

    draw_no_flights_by_month(df, airline, start_time, end_time, type)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Reset", key='button2'):
            st.session_state.month_selected = 'All'
    with col2:
        if 'month_selected' in st.session_state and st.session_state.month_selected != 'All':
            st.text("Selected month: {}".format(st.session_state.month_selected))
        else:
            "Month not selected"
    if 'month_selected' in st.session_state and st.session_state.month_selected != 'All':
        draw_flight_no(df, st.session_state.month_selected, airline, start_time, end_time, type)
        number_of_flights_by_day_of_week(df, st.session_state.month_selected, airline, start_time, end_time, type)
    else:
        number_of_flights_by_day_of_week(df, 'All', airline, start_time, end_time, type)


if __name__ == "__main__":
    set_streamlit_page()
    main()
