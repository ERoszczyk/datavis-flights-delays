import datetime

import pandas as pd
import streamlit as st

from draw_map import draw_map_with_mean_delay
from draw_statistics import draw_avg_flight_delay_by_delay_type, \
    draw_monthly_avg_flight_delay_by_month
from filters import display_time_filters

PAGE_TITLE = 'Flight Delays'
PAGE_ICON = '🌨️'
APP_SUB_TITLE = 'Data Visualisation 2023'
SIDEBAR_TITLE = 'Filter data'


def set_streamlit_page():
    st.set_page_config(PAGE_TITLE, layout="wide", page_icon=PAGE_ICON)
    st.title("Average flight delays by airport 2015")
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


def main():
    df = pd.read_csv('2015_dataset/merged_1k_sample.csv')
    start, end, min_time, max_time = display_time_filters()
    st.sidebar.button('Reset filters', on_click=reset_filters)

    draw_map_with_mean_delay(df, start, end, min_time, max_time)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Reset"):
            st.session_state.selected_airport = None
    with col2:
        if 'selected_airport' in st.session_state and st.session_state.selected_airport:
            st.text("Selected airport: {}".format(st.session_state.selected_airport))
        else:
            "No airport selected"

    col1, col2 = st.columns(2)
    with col1:
        draw_avg_flight_delay_by_delay_type(df,
                                            st.session_state.selected_airport if 'selected_airport' in st.session_state else None,
                                            start, end, min_time, max_time)
    with col2:
        draw_monthly_avg_flight_delay_by_month(df,
                                               st.session_state.selected_airport if 'selected_airport' in st.session_state else None,
                                               start, end, min_time, max_time)


if __name__ == "__main__":
    set_streamlit_page()
    main()
