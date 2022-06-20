# f1data_app
work in progress, a little data app utilizing fastf1 and streamlit to show various f1 data and analysis

streamlit has to be launched with:
streamlit run main.py --global.dataFrameSerialization="legacy"
otherwise it won't be able to process the timedelta
