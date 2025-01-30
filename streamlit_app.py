import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from arbitragelab.hedge_ratios import construct_spread
from arbitragelab.trading import BollingerBandsTradingRule
from arbitragelab.cointegration_approach import get_half_life_of_mean_reversion
from arbitragelab.cointegration_approach.johansen import JohansenPortfolio

st.write("We are going to interactively benchmark a Bollinger Bands Strategy"
         " on a chosen set of stocks.")


