import streamlit as st
st.set_page_config(page_title='F1 Data',
                   page_icon=':trophy:',
                   layout='wide',
                   )

import pandas as pd
import plotly.express as px
import fastf1 as ff1
from matplotlib import pyplot as plt
from fastf1 import plotting, utils


###
# start the app with: streamlit run main.py --global.dataFrameSerialization="legacy"
###

ff1.Cache.enable_cache(r"C:\cache")


def compare_func(driver_1, driver_2):
    laps_driver_1 = session.laps.pick_driver(driver_1)
    laps_driver_2 = session.laps.pick_driver(driver_2)
    fastest_driver_1 = laps_driver_1.pick_fastest()
    fastest_driver_2 = laps_driver_2.pick_fastest()
    telemetry_driver_1 = fastest_driver_1.get_telemetry().add_distance()
    telemetry_driver_2 = fastest_driver_2.get_telemetry().add_distance()
    team_driver_1 = fastest_driver_1['Team']
    team_driver_2 = fastest_driver_2['Team']
    delta_time, ref_tel, compare_tel = utils.delta_time(fastest_driver_1, fastest_driver_2)
    plot_size = [15, 15]
    plot_title = f'{session.event.year} {session.event.EventName} - {session.name} - {driver_1} VS {driver_2}'
    plot_ratios = [1, 3, 2, 1, 1, 2, 1]
    plot_filename = plot_title.replace(" ", "") + ".png"
    plt.rcParams['figure.figsize'] = plot_size

    fig, ax = plt.subplots(7, gridspec_kw={'height_ratios': plot_ratios})

    ax[0].title.set_text(plot_title)
    ax[0].plot(ref_tel['Distance'], delta_time)
    ax[0].axhline(0)
    ax[0].set(ylabel=f"Gap to {driver_2} (s)")

    # get speed
    ax[1].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Speed'], label=driver_1,
               color=ff1.plotting.team_color(team_driver_1))
    ax[1].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Speed'], label=driver_2,
               color=ff1.plotting.team_color(team_driver_2))
    ax[1].set(ylabel='Speed')
    ax[1].legend(loc="lower right")

    # get throttle
    ax[2].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Throttle'], label=driver_1,
               color=ff1.plotting.team_color(team_driver_1))
    ax[2].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Throttle'], label=driver_2,
               color=ff1.plotting.team_color(team_driver_2))
    ax[2].set(ylabel='Throttle')

    # get braking
    ax[3].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Brake'], label=driver_1,
               color=ff1.plotting.team_color(team_driver_1))
    ax[3].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Brake'], label=driver_2,
               color=ff1.plotting.team_color(team_driver_2))
    ax[3].set(ylabel='Brake')

    # get gear
    ax[4].plot(telemetry_driver_1['Distance'], telemetry_driver_1['nGear'], label=driver_1,
               color=ff1.plotting.team_color(team_driver_1))
    ax[4].plot(telemetry_driver_2['Distance'], telemetry_driver_2['nGear'], label=driver_2,
               color=ff1.plotting.team_color(team_driver_2))
    ax[4].set(ylabel='Gear')

    # get rpm
    ax[5].plot(telemetry_driver_1['Distance'], telemetry_driver_1['RPM'], label=driver_1,
               color=ff1.plotting.team_color(team_driver_1))
    ax[5].plot(telemetry_driver_2['Distance'], telemetry_driver_2['RPM'], label=driver_2,
               color=ff1.plotting.team_color(team_driver_2))
    ax[5].set(ylabel='RPM')

    # get drs
    ax[6].plot(telemetry_driver_1['Distance'], telemetry_driver_1['DRS'], label=driver_1,
               color=ff1.plotting.team_color(team_driver_1))
    ax[6].plot(telemetry_driver_2['Distance'], telemetry_driver_2['DRS'], label=driver_2,
               color=ff1.plotting.team_color(team_driver_2))
    ax[6].set(ylabel='DRS')
    ax[6].set(xlabel='Lap distance (meters)')

    # hide labels
    for a in ax.flat:
        a.label_outer()

    plt.show()



# setting up the control panel
st.sidebar.header('Control Panel')
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

driver1 = st.sidebar.selectbox(
    'Pick driver 1',
    session.results['LastName']
)

driver2 = st.sidebar.selectbox(
    'Pick driver 2',
    session.results['LastName']
)

st.table(session.results)


# if st.button('Compare'):
#     compare_func(driver1, driver2)



# this shows the whole season:
#st.table(clean_schedule)
#df = ff1.get_session(season)
