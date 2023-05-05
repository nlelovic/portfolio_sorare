import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Initialize connection.
conn = st.experimental_connection('snowpark')

st.header("Descriptive statistics")

# price distribution of transactions in EUR for each rarity level

#released_comps = "select display_name from sorare_competition where released = 1;"

#rarity_select = st.selectbox("Pick a card rarity", options=["limited","rare","super_rare","unique"])

#comps_select = st.selectbox("Pick a football league", options=released_comps)

#price_history = "select t1.price_eur from sorare_price_history as t1 inner join sorare_cards as t2 on t1.cards_card_id = t2.card_id where t2.rarity = '{rarity_select}' and t1.price_eur != 0;"
price_history = "select ln(t1.price_eur), t2.rarity from sorare_price_history as t1 inner join sorare_cards as t2 on t1.cards_card_id = t2.card_id where t1.price_eur != 0;"

result_price_history = conn.query(price_history, ttl=24*3600)

col1_dist , col2_dist = st.columns((1,1))
#col1_dist , col2_dist, col3_dist, col4_dist = st.columns((1,1,1,1))

with col1_dist:
    fig_violin, ax = plt.subplots()
    ax = sns.violinplot(x="RARITY", y="LN(T1.PRICE_EUR)", data=result_price_history)
    st.pyplot(fig_violin)

with col2_dist:
    st.empty()

