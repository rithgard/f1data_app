import pandas as pd
import plotly.express as px
import streamlit as st
import fastf1 as ff1

# input a location on your pc
ff1.Cache.enable_cache(r"your cache location")

st.set_page_config(page_title='F1 Data',
                   page_icon=':trophy:',
                   layout='wide',
                   )
# seting up the sidebar and season selectbox
st.sidebar.header('filters and shit')
season = st.sidebar.selectbox(
    'Which season?',
    (2022, 2021, 2020, 2019, 2018)
)


schedule = ff1.get_event_schedule(season)
clean_schedule = schedule[['Country', 'Location', 'OfficialEventName', 'EventDate', 'EventName']]


picked_race = st.sidebar.selectbox(
    'Pick a race',
    clean_schedule['EventName']
)

qor = st.sidebar.selectbox(
    'Qualifying or Race?',
    ('Q', 'R')
)

session = ff1.get_session(season, picked_race, qor)
session.load()
st.table(session.results)

# this shows the whole season:
#st.table(clean_schedule)
#df = ff1.get_session(season)


















