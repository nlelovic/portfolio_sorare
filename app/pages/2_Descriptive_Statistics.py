import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly_resampler import FigureResampler
import numpy as np


# Initialize connection.
conn = st.experimental_connection('snowpark')

st.header("Descriptive statistics")

# price distribution of transactions in EUR

col1_dist , col2_dist = st.columns((2,1))

with col1_dist:
    # get price history from db
    price_history = """
    select PRICE_EUR from SORARE_PRICE_HISTORY
    """
    result_price_history = conn.query(price_history, ttl=24*3600)

    col_name = result_price_history.columns[0]
    
    #st.write(result_price_history.loc[:, col_name])
    descr_price_history = result_price_history.describe()
    IQR_price_history = descr_price_history.loc["75%"][0] - descr_price_history.loc["25%"][0]
    st.write(result_price_history.describe())

    opt_binsize_price_history = int(np.round(descr_price_history.loc["count"][0] * IQR_price_history /100))
    st.write(opt_binsize_price_history)

    #fig_price_history = px.histogram(result_price_history, x=col_name, marginal="violin", nbins=opt_binsize_price_history)
    #st.plotly_chart(fig_price_history)

    #fig_price_history = ff.create_distplot(result_price_history, group_labels=[col_name])
    #st.plotly_chart(fig_price_history)

    # Using figure resampler 
    fig_price_history = FigureResampler(go.Figure())
    fig_price_history.add_trace(go.Histogram(x=result_price_history.iloc[:, 0]))
    #st.plotly_chart(fig_price_history)



with col2_dist:
    st.empty()


if __name__ == "__main__":
    from multiprocessing import Process

    port = 9022
    proc = Process(
        target=fig_price_history.show_dash, kwargs=dict(mode="external", port=port)
    ).start()

    import streamlit.components.v1 as components
    components.iframe(f"http://localhost:{port}", height=700)
