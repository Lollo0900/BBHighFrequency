import streamlit as st
import numpy as np
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from arbitragelab.hedge_ratios import construct_spread
from arbitragelab.trading import BollingerBandsTradingRule
from arbitragelab.cointegration_approach import get_half_life_of_mean_reversion
from arbitragelab.cointegration_approach.johansen import JohansenPortfolio

st.write("We are going to interactively benchmark a Bollinger Bands Strategy"
         " on a chosen set of stocks.")

# Using object notation
stock_list = st.sidebar.text_input(
    "Input your portfolio Ticker:", "MSFT AAPL",
    placeholder="e.g. MSFT AAPL"
)
# Using "with" notation
with (st.sidebar):
    start_date = st.text_input(
        "Select the timeframe on which to run the strategy.\n Input the start date:", "2023-03-01",
        placeholder="e.g. %Y-%m-%d"
    )

    end_date = st.text_input(
        "Input the end date:", "2023-06-01",
        placeholder="e.g. %Y-%m-%d"
    )

    johansen_data = st.text_input("Input the amount of data (in absolute units)\n"
                                  " to be used  for the Johansen Test:", "10",
                                  placeholder="e.g. 15"
                                  )

    options = {"No deterministic Term": -1, "Constant Term": 0, "Linear Trend": 1}
    johansen_option = st.selectbox("Select the Johansen test model:", options.keys())
    johansen_option = options[johansen_option]

    lookback = st.text_input("Input the lookback window for the moving averages \n "
                             "of the Bollinger Band strategy", "5",
                             placeholder="e.g. 5"
                             )
    lookback = int(lookback)

    entry_z = st.slider("Select the entry Z-score for the strategy:", min_value=0.0, max_value=5.0, value=1.5, step=0.1)

    exit_z = st.slider("Select the exit Z-score for the strategy:", min_value=0.0, max_value=5.0, value=2.0, step=0.1)

    risk_free = st.text_input("Input the risk-free interest rate (in %) to be used to compute the Sharpe ratio", "3",
                              placeholder="e.g. 5"
                              )
    risk_free = float(risk_free)

df = yf.download(stock_list.replace(" ", ", "), start=start_date, end=end_date, auto_adjust=False)
st.write("Here we summarise the historical data for the chosen stocks.")
st.dataframe(df, height=200)

st.write("An initial Johansen test on the first " + johansen_data + " data entries gives the following results:")
j_portfolio = JohansenPortfolio()
# Fitting the data on a dataset
j_portfolio.fit(df['Adj Close'].iloc[:int(johansen_data)], det_order=johansen_option)
# Getting results of the eigenvalue and trace Johansen tests
j_eigenvalue_statistics = j_portfolio.johansen_eigen_statistic
j_trace_statistics = j_portfolio.johansen_trace_statistic
j_cointegration_vectors = j_portfolio.cointegration_vectors
j_hedge_ratios = j_portfolio.hedge_ratios

spread = construct_spread(df['Adj Close'].iloc[:int(johansen_data)], hedge_ratios=j_hedge_ratios.iloc[0])
half_life = get_half_life_of_mean_reversion(spread)

data = {'Eigen Statistic': j_eigenvalue_statistics.iloc[-1], 'Confidence 90%': j_eigenvalue_statistics.iloc[0],
        'Confidence 95%': j_eigenvalue_statistics.iloc[1], 'Confidence 99%': j_eigenvalue_statistics.iloc[2]}
jtest_eigen = pd.DataFrame(data)
st.table(jtest_eigen)
data = {'Trace Statistic': j_trace_statistics.iloc[-1], 'Confidence 90%': j_trace_statistics.iloc[0],
        'Confidence 95%': j_trace_statistics.iloc[1], 'Confidence 99%': j_trace_statistics.iloc[2]}
jtest_trace = pd.DataFrame(data)
st.table(jtest_trace)

st.write("The test has an half life of:", half_life, ", and leads to the following hedge ratios:")
st.table(j_hedge_ratios)

st.write("Given those hedge rations, the spread of associated the portfolio evolves like:")
spread = construct_spread(df['Adj Close'].iloc[int(johansen_data):], hedge_ratios=j_hedge_ratios.iloc[0])

fig = plt.figure(1)
plt.title("Spread value over time")
plt.plot(spread)
plt.grid()
st.pyplot(fig)

# Creating a strategy
strategy = BollingerBandsTradingRule(sma_window=lookback, std_window=lookback,
                                     entry_z_score=entry_z, exit_z_score_delta=exit_z)
strategy.update_spread_value(spread[0])
# Feeding spread values to the strategy one by one
for time, value in spread.items():
    strategy.update_spread_value(value)
    # Checking if logic for opening a trade is triggered
    trade, side = strategy.check_entry_signal()
    # Adding a trade if we decide to trade signal
    if trade:
        strategy.add_trade(start_timestamp=time, side_prediction=side)
    # Update trades, close if logic is triggered
    close = strategy.update_trades(update_timestamp=time)
# Checking currently open trades
open_trades = strategy.open_trades
# Checking all closed trades
closed_trades = strategy.closed_trades

open_trades_df = pd.DataFrame(open_trades)
closed_trades_df = pd.DataFrame(closed_trades)

if bool(open_trades):
    open_trades_df.drop('uuid', axis=0, inplace=True)
copy = closed_trades_df.copy()
if bool(closed_trades):
    closed_trades_df.drop('t1', axis=0, inplace=True)
    closed_trades_df.drop('uuid', axis=0, inplace=True)
    closed_trades_df.loc['t1'] = copy.loc['t1']

st.write("Running a Bollinger Band Strategy  with lookback ", lookback,
         ", entry Z-score ", entry_z, ", exit Z-score ", exit_z, ", on "
         "the Adjusted Closed prices from " + start_date + " to " + end_date +
         ",\n results in the following closed trades:")
st.dataframe(closed_trades_df)
st.write("Whilst the open trades at the end date are:")
st.dataframe(open_trades_df)

st.write("Each closed trade results in a return of:")
returns = {"Trade": None, "Return (in %)": None}
returns = pd.DataFrame(returns, index=[0])
for key in closed_trades.keys():
    returns.loc[len(returns)] = [pd.Timestamp(key),
                                 100 * (closed_trades[key]['end_value'] - closed_trades[key]['start_value']) /
                                 closed_trades[key]['start_value']]
ave_r = np.mean(returns["Return (in %)"])
sigma_r = np.std(returns["Return (in %)"])
sharpe = (ave_r - risk_free) / sigma_r

st.dataframe(returns)
st.write("Resulting in an average return of ", "%.1f" % ave_r, "%, volatility of", "%.1f" % sigma_r, "% with a Sharpe "
         "Ratio of ", "%.1f" % sharpe)
