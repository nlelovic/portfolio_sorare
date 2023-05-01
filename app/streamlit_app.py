import streamlit as st
import pandas as pd
import numpy as np

# Initialize connection.
conn = st.experimental_connection('snowpark')

# Perform query. Caching 10 mins -> ttl=600 and no caching -> ttl=0
df = conn.query('select top 5 * from SORARE_COMPETITION;', ttl=0)

for row in df.itertuples():
    st.write(row)