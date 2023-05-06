import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from scipy import stats


# Initialize connection.
conn = st.experimental_connection('snowpark')

st.header("Descriptive statistics")

# price distribution of transactions in EUR for each rarity level

#released_comps = "select display_name from sorare_competition where released = 1;"

#rarity_select = st.selectbox("Pick a card rarity", options=["limited","rare","super_rare","unique"])

#comps_select = st.selectbox("Pick a football league", options=released_comps)

#price_history = "select t1.price_eur from sorare_price_history as t1 inner join sorare_cards as t2 on t1.cards_card_id = t2.card_id where t2.rarity = '{rarity_select}' and t1.price_eur != 0;"
price_history = "select ln(t1.price_eur), t2.rarity, t1.price_eur from sorare_price_history as t1 inner join sorare_cards as t2 on t1.cards_card_id = t2.card_id where t1.price_eur != 0;"

result_price_history = conn.query(price_history, ttl=24*3600)

col1_dist , col2_dist = st.columns((1,1))
#col1_dist , col2_dist, col3_dist, col4_dist = st.columns((1,1,1,1))

with col1_dist:

    st.caption("Logarithmic Price distribution of transactions in EUR for each rarity level")

    fig_violin, ax = plt.subplots()
    ax = sns.violinplot(x="RARITY", y="LN(T1.PRICE_EUR)", data=result_price_history)
    st.pyplot(fig_violin)

    del(fig_violin,ax)

    st.write("one can observe the logical relationship between different scarcity levels and the market prices of the cards.")

with col2_dist:

    st.caption("Statistics divided by rarity levels.")


    st.dataframe(result_price_history[["PRICE_EUR","RARITY"]].groupby("RARITY").describe().T)

    st.write("Important take of the statistics, prices are distributed non normally and are right skewed in the distribution.")

st.subheader("Now we take a closer look at the distribution of the logarithmic price of the super rare cards:")

st.write("It is necessary to use a logarithmic scale for the price distribution, since the price is extremely different for different players. Differences between prices are better interpretable with the logarithmic scale.")

super_rare = result_price_history[result_price_history["RARITY"] == "super_rare"]

scaler=StandardScaler()
X_std=scaler.fit_transform(super_rare["LN(T1.PRICE_EUR)"].values.reshape(-1,1))
super_rare["LN(T1.PRICE_EUR)"] = X_std.reshape(-1)

fig_superrare_log = ff.create_distplot([list(super_rare["LN(T1.PRICE_EUR)"])], ["LN(PRICE_EUR)"])
st.plotly_chart(fig_superrare_log)

# fig_superrare = ff.create_distplot([list(super_rare["PRICE_EUR"])], ["PRICE_EUR"])
# st.plotly_chart(fig_superrare)

alpha = 0.05
k2,p = stats.normaltest(super_rare["LN(T1.PRICE_EUR)"])

st.markdown(
    """
    In order to test whether the log prices are normally distributed or not, we need to conduct a statistical hypothesis test.
    The null hypotheis of the statistical test is set as "The data is normally distributed." For the computation, scipy.stats.normaltest from D'Agostino is used.

    After the computation, we find:
    """
)

if p < alpha:
    st.write("The null hypothesis can be rejected. So the log prices are not normally distributed.")
else:
    st.write("The null hypothesis cannot be rejected. So the log prices are normally distributed.")

st.markdown(
    """
    This result allows to get a sense about how the data is distributed. If the underlying data is normally distributed, then further assumptions about the price process can be derived and one can apply other more advanced Econometric methods to do a more thorough analysis.

    Further analysis will not be made, as it is out of scope for this project and Streamlit application demonstration. But still. It is a valuable result to know, that the price process of the super rare cards is not normally distributed.
    """
)