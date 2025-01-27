import streamlit as st
import yfinance as yf

st.write("Here we are going to interactively benchmark a Bollinger Bands Strategy"
         "on a chosen set of stocks")

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

df=yf.download(stock_list.replace(" ",", "),start=start_date,end=end_date,auto_adjust=False)
st.dataframe(df,height=200)
