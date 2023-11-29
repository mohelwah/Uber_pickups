import streamlit as st
import pandas as pd
import numpy as np

st.title("Uber pickups in NYC")

DATE_COLUMN = "date/time"
DATA_URL = (
    "https://s3-us-west-2.amazonaws.com/"
    "streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercas = lambda x: str(x).lower()
    data.rename(lowercas, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text("Loading data...")

data = load_data(10000)

data_load_state.text('Loading data .... done (using cache) !') 

if st.checkbox("Show row data"):
    st.subheader("Raw data")
    st.dataframe(data)

st.subheader('Number of pickups by hour')

hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.bar_chart(hist_values)

st.subheader('Map of all pickups')

st.map(data)

hour_to_filer = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filer]

st.subheader(f"Maps of all pickups at {hour_to_filer}:00")

st.map(filtered_data)