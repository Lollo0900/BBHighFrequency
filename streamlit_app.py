import streamlit as st

st.write("Hello there")

import streamlit as st

# Using object notation
stock_list = st.sidebar.text_input(
    "How would you like to be contacted?", "MSFT AAPL"
    placeholder="e.g. MSFT AAPL"
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )


