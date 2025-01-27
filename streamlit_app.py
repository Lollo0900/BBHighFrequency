import streamlit as st
import yfinance as yf

st.write("Hello there")

import streamlit as st

# Using object notation
stock_list = st.sidebar.text_input(
    "Input your portfolio Ticker:", "MSFT AAPL",
    placeholder="e.g. MSFT AAPL"
)
# Using "with" notation
with st.sidebar:
    start_date = st.text_input(
        "Select the timeframe on which to run the strategy.\n Input the start date:","2023-03-01",
        placeholder="e.g. %Y-%m-%d"
    )
    end_date = st.text_input(
        "Input the end date:","2023-06-01",
        placeholder="e.g. %Y-%m-%d"
    )

df=yf.download(stock_list.replace(" ",", "),start=start_date,end=end_date)
st.write(df.shape)
st.dataframe(df,height=200)
st.dataframe(df["Adj Close"])