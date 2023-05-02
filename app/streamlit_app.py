import streamlit as st
import pandas as pd
import numpy as np

# page config
st.set_page_config(
    page_title="Sorare NFT Cards Exploration and Analysis",
    #page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# Initialize connection.
conn = st.experimental_connection('snowpark')

# Perform query. Caching 10 mins -> ttl=600 and no caching -> ttl=0
df = conn.query('select top 5 * from SORARE_COMPETITION;', ttl=0)

st.dataframe(df)