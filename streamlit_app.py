import streamlit as st

st.write("Hello there")

import streamlit as st

# Using object notation
add_selectbox = st.sidebar.text_inpput(
    "How would you like to be contacted?",
    
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )


