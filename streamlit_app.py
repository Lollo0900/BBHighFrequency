import streamlit as st
import yfinance as yf

st.write("Hello there")

import streamlit as st

# Using object notation
stock_list = st.sidebar.text_input(
    "Input your portfolio Ticker", "MSFT AAPL",
    placeholder="e.g. MSFT AAPL"
)
# Using "with" notation
with st.sidebar:
    timeframe = st.select_slider(
        "Select the timeframe on which to run the strategy",
        ('5y','1y','9mo','3mo','1mo','5d','1d')
    )

df=yf.download(stock_list.split(),timeframe)
st.write(timeframe)
st.dataframe(df,height=100)