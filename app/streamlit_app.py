import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np

# page config
st.set_page_config(
    page_title="Sorare NFT Cards Exploration and Analysis",
    page_icon="⚽",
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
# df = conn.query('select top 5 * from SORARE_COMPETITION;', ttl=0)

# st.dataframe(df)


# Title Picture
# Iframe Sorare title picture

c1, c2, c3 = st.columns((6,1,9))

with c1:
    # st.image(components.html(
    #     """
    #     <a href="https://vtlogo.com/sorare-vector-logo-svg/" target="_blank"><img src="https://vtlogo.com/wp-content/uploads/2022/09/sorare-vector-logo-2022.png" /></a>
    #     """,
    #     height=450
    # ))
    st.image("https://vtlogo.com/wp-content/uploads/2022/09/sorare-vector-logo-2022.png")
with c2:
    st.empty()
with c3:
    # What is Sorare? 

    st.header("What is Sorare?")

    st.caption("Like Panini cards but with NFT technology and a fantasy game.")

    st.write("""Sorare was funded 5 years ago in 2018 by a French startup based in Paris. Basically, Sorare built a fantasy game with NFTs.
                You can purchase various cards of real stars in football and use them to compete in different competitions against other
                NFT card holders. Over the years Sorare managed to incorporate more and more european football leagues and further stepped into
                new sports markets like the MLB or NBA.
            """)

st.subheader("What can you expect from this Streamlit app and why was it created?")

st.write(
    """
    This app will allow you to browse through the database of the Sorare football cards and also do some basic analysis backed by machine learning methods.
    It is a product of my Master's studies, where newly acquired machine learning and big data techniques should be applied on a dataset of choice.
    This project is part of my data science portfolio to demonstrate my skill set and capabilities as a Data Scientist. And of course offer you a nice experience!
    Make sure to check out the About page, where you can find more info about Sorare and also about me.
    Have fun!
    """
)

# Header Title Page
query_header = """select    (
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
           select sum(PRICE_EUR)
           from SORARE_PRICE_HISTORY
           ) as Trading_Volume_EUR,
           (
           select sum(PRICE)
           from SORARE_PRICE_HISTORY
           ) as Trading_Volume_ETH,
           (
           select count(*)
           from SORARE_PRICE_HISTORY
           ) as Transactions_Count,
           (
           select sum(GOALS)
           from SORARE_STATS
           ) as Goals_Count,
           (
           select sum(MINUTES_PLAYED)
           from SORARE_STATS
           ) as Minutes_Played
           ;"""


#@st.cache_data(ttl=24*3600)
results_header = conn.query(query_header, ttl=24*3600)

st.subheader("Database information")
st.write("The database was created in January 2021. Therefore, the entries are only updated until that date. Nevertheless, the focus is to demonstrate a nice Streamlit powered dashboard with data stored in Snowflake.")
st.write(f"The database consist of {results_header.iloc[0][0]:,.0f} players, {results_header.iloc[0][1]:.0f} cards, {results_header.iloc[0][2]:.0f} competitions, and {results_header.iloc[0][3]:.0f} clubs. The trading volume amounts to {results_header.iloc[0][4]:,.2f} EUR or {results_header.iloc[0][5]:,.2f} ETH with {results_header.iloc[0][6]:,.0f} transactions. Also {results_header.iloc[0][7]:,.0f} goals were scored and {results_header.iloc[0][8]:,.0f} minutes were played in real life.")

# Random card generator after picking a players name

player_names = conn.query("select DISPLAY_NAME from SORARE_PLAYER;")

col1, col2, col3 = st.columns((2,1,1))

with col1:
    name_picture = st.selectbox("Pick a player", options=player_names)

    query_picture = f"select t2.DISPLAY_NAME, t1.PICTURE_URL from sorare_cards as t1 INNER join sorare_player as t2 on t1.player_id = t2.player_id where t2.display_name = '{name_picture}' Limit 1;"

    results_picture = conn.query(query_picture, ttl=24*3600)
    
    ## Table for player informations

    # Cache the dataframe so it's only loaded once
    #@st.cache_data

    player_info = f"select t1.Position, t1.active_club_name, t1.Subscription_count, t1.age, t1.height,  t1.nationality, t2.goals, t2.appearances, t2.assists, t2.yellow_cards, t2.red_cards, t2.minutes_played from SORARE_Player as t1 inner join sorare_stats as t2 on t1.player_id = t2.STATS_PLAYER_ID where t1.Display_Name = '{name_picture}';" 
                    

    result_player_info = conn.query(player_info, ttl=24*3600)
    
    


    # Display the dataframe and allow the user to stretch the dataframe
    # across the full width of the container, based on the checkbox value
    st.dataframe(result_player_info.T, use_container_width=True)
    

with col2:
    st.empty()

with col3:
    st.image(results_picture.iloc[0][1])
    
