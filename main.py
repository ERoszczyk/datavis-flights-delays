import streamlit as st
from st_pages import Page, show_pages

show_pages(
    [
        Page("pages/Airport.py", "Delay By Airport", "📌"),
        Page("pages/Routes.py", "Delay By Routes", "🗺"),
        Page("pages/Time.py", "Delay By Time", "📅"),
        Page("pages/Airlines.py", "Delay By Airlines", "🛫")
    ]
)

st.rerun()
