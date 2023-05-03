import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np

# page config
st.set_page_config(
    page_title="Sorare NFT Cards Exploration and Analysis",
    page_icon="🧊",
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


# Title Picture
# Iframe Sorare title picture

components.html(
    """
    <a href="https://vtlogo.com/sorare-vector-logo-svg/" target="_blank"><img src="https://vtlogo.com/wp-content/uploads/2022/09/sorare-vector-logo-2022.png" /></a>
    """,
    height=450
)


# Header Title Page
# some queries
queries_header = """select    (
           select count(*)
           from SORARE_PLAYER
           ) as Player_Count,
           (
           select count(*)
           from SORARE_CARDS
           ) as Card_Count,
           (
           select count(*)
           from SORARE_COMPETITION
           ) as Competition_Count,
           (
           select count(*)
           from SORARE_CLUB
           ) as Club_Count,
           (
           select count(*)
           from SORARE_PRICE_HISTORY
           ) as Trading_Volume_EUR,
           (
           select count(*)
           from SORARE_PRICE_HISTORY
           ) as Trading_Volume_ETH,
           (
           select count(*)
           from SORARE_PRICE_HISTORY
           ) as Transactions_Count,
           (
           select count(*)
           from SORARE_STATS
           ) as Goals_Count,
           (
           select count(*)
           from SORARE_STATS
           ) as Minutes_Played
           ;"""


#@st.cache_data(ttl=24*3600)
results_header = conn.query(queries_header, ttl=24*3600)#.iloc[0][0]


st.write(f"The database consist of {results_header.iloc[0][0]:,} players, {results_header.iloc[0][1]} cards, {results_header.iloc[0][2]} competitions, and {results_header.iloc[0][3]} clubs. The trading volume amounts to {results_header.iloc[0][4]:,.2f} EUR or {results_header.iloc[0][5]:,.2f} ETH with {results_header.iloc[0][6]:,} transactions. Also {results_header.iloc[0][7]:,} goals were scored and {results_header.iloc[0][8]:,} minutes were played.")

#st.write(results_header.iloc[0][0])