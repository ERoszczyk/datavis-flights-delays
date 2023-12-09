import pandas as pd
import streamlit as st

from draw_statistics import mean_arr_dep_by_airlines, cancellation_rate_by_airlines
from filters import display_time_filters, display_airlines_filter

PAGE_TITLE = 'Flight Delays'
PAGE_ICON = '🌨🛫'
APP_SUB_TITLE = 'Data Visualisation 2023'
SIDEBAR_TITLE = 'Filter data'
import datetime


def reset_filters():
    st.session_state.airlines = []
    st.session_state.time = (datetime.time(0, 0), datetime.time(23, 59))
    st.session_state.start_date = pd.to_datetime("2015-01-01", format="%Y-%m-%d")
    st.session_state.end_date = pd.to_datetime("2015-12-31", format="%Y-%m-%d")


def set_streamlit_page():
    st.set_page_config(PAGE_TITLE, layout="wide", page_icon=PAGE_ICON)
    st.title("Average flight delays by airlines 2015")
    st.sidebar.title(SIDEBAR_TITLE)
    st.markdown("""
      <style>
        .st-emotion-cache-16txtl3 {
          margin-top: -75px;
        }
      </style>
    """, unsafe_allow_html=True)


def main():
    df = pd.read_csv('2015_dataset/merged_1k_sample.csv')
    df_airlines = pd.read_csv('2015_dataset/airlines.csv')

    start, end, min_time, max_time = display_time_filters()
    airlines = display_airlines_filter(df_airlines)
    st.sidebar.button('Reset filters', on_click=reset_filters)

    mean_arr_dep_by_airlines(df, start, end, min_time, max_time, airlines)
    cancellation_rate_by_airlines(df, start, end, airlines)


if __name__ == "__main__":
    set_streamlit_page()
    main()
